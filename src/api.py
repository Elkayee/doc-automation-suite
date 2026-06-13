import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Ensure the root of the workspace is in the python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.assembler import DocumentAssembler
from src.core.docx_builder import DocxBuilder
from src.core.logger import logger
from src.core.template_manager import TemplateManager

app = FastAPI(
    title="Doc Automation Suite API",
    description="REST API interface for document assembly and automated rendering pipelines.",
    version="0.1.0"
)


class CompileRequest(BaseModel):
    workspace_name: str
    docx_out: str | None = None
    md_out: str | None = None
    cache_dir: str | None = None


class CreateRequest(BaseModel):
    name: str
    template: str


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Doc Automation Suite API",
        "version": "0.1.0",
        "documentation": "/docs"
    }


@app.get("/templates")
def list_templates():
    try:
        templates_dir = BASE_DIR / "templates"
        manager = TemplateManager(templates_dir)
        templates = manager.list_templates()
        return {
            "templates": {
                tid: {
                    "name": t.name,
                    "type": t.type,
                    "description": t.description,
                    "required_files": t.required_files,
                    "docx_template": t.docx_template
                }
                for tid, t in templates.items()
            }
        }
    except Exception as e:
        logger.error(f"Failed to list templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _secure_resolve(base_path: Path, sub_path: str) -> Path:
    """Securely resolves a sub_path within base_path to prevent path traversal."""
    resolved = (base_path / sub_path).resolve()
    if not resolved.is_relative_to(base_path.resolve()):
        raise HTTPException(status_code=400, detail="Invalid path: Path traversal detected.")
    return resolved


@app.post("/workspaces/create")
def create_workspace(req: CreateRequest):
    templates_dir = BASE_DIR / "templates"
    workspaces_dir = BASE_DIR / "workspaces"

    dest_dir = _secure_resolve(workspaces_dir, req.name)

    manager = TemplateManager(templates_dir)

    if dest_dir.exists():
        raise HTTPException(status_code=400, detail=f"Workspace '{req.name}' already exists.")

    try:
        logger.info(f"API: Creating project '{req.name}' from template '{req.template}'...")
        manager.create_project(req.template, dest_dir)
        return {
            "success": True,
            "message": f"Workspace '{req.name}' successfully created.",
            "path": str(dest_dir)
        }
    except Exception as e:
        logger.error(f"API: Failed to create project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workspaces/compile")
def compile_workspace(req: CompileRequest):
    workspaces_dir = BASE_DIR / "workspaces"

    try:
        workspace_dir = _secure_resolve(workspaces_dir, req.workspace_name)
    except HTTPException:
        raise HTTPException(status_code=400, detail="Invalid workspace name: Path traversal detected.")

    if not workspace_dir.exists() or not workspace_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"Workspace path not found: {req.workspace_name}")

    logger.info(f"API: Starting compile pipeline for: {workspace_dir.name}")

    build_dir = workspace_dir / "build"
    build_dir.mkdir(exist_ok=True)

    try:
        # 🛡️ Sentinel: Validate user-provided output paths against path traversal to prevent arbitrary file writes
        final_md_out = _secure_resolve(build_dir, req.md_out) if req.md_out else build_dir / "assembled.md"
        final_docx_out = _secure_resolve(build_dir, req.docx_out) if req.docx_out else build_dir / f"{workspace_dir.name}.docx"
        final_cache_dir = _secure_resolve(build_dir, req.cache_dir) if req.cache_dir else build_dir / "img_cache"
    except HTTPException:
        raise HTTPException(status_code=400, detail="Invalid output path: Path traversal detected.")

    final_cache_dir.mkdir(exist_ok=True)

    try:
        # Assemble
        assembler = DocumentAssembler(workspace_dir)
        final_md, chapter_files = assembler.save_assembled_for_export(final_md_out)

        # Render
        builder = DocxBuilder(workspace_dir)
        builder.build_from_markdown(str(final_md_out), final_cache_dir)
        builder.save(final_docx_out)

        return {
            "success": True,
            "message": "Compilation successful",
            "assembled_markdown": str(final_md_out),
            "compiled_docx": str(final_docx_out),
            "chapters_processed": len(chapter_files)
        }
    except Exception as e:
        logger.error(f"API: Compile failed for {workspace_dir.name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Compile failed: {e}")
