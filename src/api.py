import sys
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Ensure the root of the workspace is in the python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.batch import run_batch
from src.core.export import ExportValidationError, compile_document
from src.core.logger import logger
from src.core.template_manager import TemplateManager
from src.core.project_paths import workspace_path
from src.core.renderers import renderer_status
from src.core.runtime import VERSION, data_root, resource_root

BASE_DIR = resource_root()

app = FastAPI(
    title='Doc Automation Suite API',
    description='REST API interface for document assembly and automated rendering pipelines.',
    version=VERSION,
)


class CompileRequest(BaseModel):
    workspace_name: str
    docx_out: str | None = None
    md_out: str | None = None
    cache_dir: str | None = None
    pdf_out: str | None = None
    formats: list[Literal['docx', 'pdf']] = ['docx']
    mode: Literal['draft', 'final'] = 'draft'
    engine: Literal['auto', 'builtin', 'academic'] = 'auto'
    metadata: dict | None = None


class BatchRequest(BaseModel):
    jobs: list[CompileRequest]


class CreateRequest(BaseModel):
    name: str
    template: str


@app.get('/')
def read_root():
    return {'status': 'online', 'service': 'Doc Automation Suite API', 'version': VERSION, 'documentation': '/docs'}


@app.get('/capabilities')
def capabilities():
    return {'formats': ['docx', 'pdf'], 'engines': ['auto', 'builtin', 'academic'],
            'renderers': {name: path is not None for name, path in renderer_status().items()}}


@app.get('/templates')
def list_templates():
    try:
        templates_dir = BASE_DIR / 'templates'
        manager = TemplateManager(templates_dir)
        templates = manager.list_templates()
        return {
            'templates': {
                tid: {
                    'name': t.name,
                    'type': t.type,
                    'description': t.description,
                    'required_files': t.required_files,
                    'docx_template': t.docx_template,
                }
                for tid, t in templates.items()
            }
        }
    except Exception as e:
        logger.error(f'Failed to list templates: {e}')
        raise HTTPException(status_code=500, detail=str(e))


def _secure_resolve(base_path: Path, sub_path: str) -> Path:
    """Securely resolves a sub_path within base_path to prevent path traversal."""
    resolved = (base_path / sub_path).resolve()
    if not resolved.is_relative_to(base_path.resolve()):
        raise HTTPException(status_code=400, detail='Invalid path: Path traversal detected.')
    return resolved


@app.post('/workspaces/create')
def create_workspace(req: CreateRequest):
    templates_dir = BASE_DIR / 'templates'
    workspaces_dir = data_root(BASE_DIR) / 'workspaces'

    try:
        dest_dir = workspace_path(workspaces_dir, req.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    manager = TemplateManager(templates_dir)

    if dest_dir.exists():
        raise HTTPException(status_code=400, detail=f"Workspace '{req.name}' already exists.")

    try:
        logger.info(f"API: Creating project '{req.name}' from template '{req.template}'...")
        manager.create_project(req.template, dest_dir)
        return {'success': True, 'message': f"Workspace '{req.name}' successfully created.", 'path': str(dest_dir)}
    except Exception as e:
        logger.error(f'API: Failed to create project: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/workspaces/compile')
def compile_workspace(req: CompileRequest):
    workspaces_dir = data_root(BASE_DIR) / 'workspaces'

    try:
        workspace_dir = _secure_resolve(workspaces_dir, req.workspace_name)
    except HTTPException:
        raise HTTPException(status_code=400, detail='Invalid workspace name: Path traversal detected.')

    if not workspace_dir.exists() or not workspace_dir.is_dir():
        raise HTTPException(status_code=404, detail=f'Workspace path not found: {req.workspace_name}')

    try:
        result = compile_document(workspace_dir, **_compile_options(req, workspace_dir))
        return {'message': 'Compilation successful', **result.to_dict()}
    except HTTPException:
        raise
    except ExportValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors) from exc
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as e:
        logger.error(f'API: Compile failed for {workspace_dir.name}: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail=f'Compile failed: {e}')


def _compile_options(req, workspace_dir):
    options = {'formats': req.formats, 'mode': req.mode, 'engine': req.engine, 'metadata': req.metadata}
    for request_name, core_name in [('docx_out', 'docx_out'), ('md_out', 'md_out'),
                                   ('pdf_out', 'pdf_out'), ('cache_dir', 'cache_dir')]:
        path = getattr(req, request_name)
        if path:
            options[core_name] = _secure_resolve(workspace_dir, path)
    return options


@app.post('/workspaces/batch')
def batch_workspaces(req: BatchRequest):
    base = data_root(BASE_DIR) / 'workspaces'
    jobs = []
    for request in req.jobs:
        try:
            workspace = _secure_resolve(base, request.workspace_name)
            jobs.append({'workspace': str(workspace), **_compile_options(request, workspace)})
        except HTTPException as exc:
            jobs.append({'workspace': request.workspace_name, '_error': exc.detail})
    return run_batch(jobs, base_dir=base)
