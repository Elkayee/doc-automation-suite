import sys
from pathlib import Path
import click

# Ensure the root directory of the workspace is in the python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.logger import logger
from src.core.assembler import DocumentAssembler
from src.core.docx_builder import DocxBuilder
from src.core.template_manager import TemplateManager


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Doc Automation Suite CLI toolkit."""
    pass


@cli.command(name="compile")
@click.argument("workspace_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--docx-out", type=click.Path(path_type=Path), help="Custom path for the compiled DOCX file.")
@click.option("--md-out", type=click.Path(path_type=Path), help="Custom path for the assembled Markdown file.")
@click.option("--cache-dir", type=click.Path(path_type=Path), help="Custom path for rendering image cache.")
def compile_workspace(workspace_dir: Path, docx_out: Path, md_out: Path, cache_dir: Path):
    """Assembles and compiles a markdown workspace into a Word document."""
    workspace_dir = workspace_dir.resolve()
    logger.info(f"Starting compile pipeline for workspace: {workspace_dir.name}")

    # 1. Determine paths
    build_dir = workspace_dir / "build"
    build_dir.mkdir(exist_ok=True)

    final_md_out = md_out or build_dir / "assembled.md"
    final_docx_out = docx_out or build_dir / f"{workspace_dir.name}.docx"
    final_cache_dir = cache_dir or build_dir / "img_cache"

    final_cache_dir.mkdir(exist_ok=True)

    try:
        # 2. Assemble Markdown
        logger.info("Step 1: Assembling chapter markdown files...")
        assembler = DocumentAssembler(workspace_dir)
        final_md, chapter_files = assembler.save_assembled_for_export(final_md_out)

        logger.info(f"Successfully assembled {len(chapter_files)} chapters -> {final_md_out.name}")

        # 3. Build DOCX
        logger.info("Step 2: Rendering Markdown to DOCX...")
        builder = DocxBuilder(workspace_dir)
        builder.build_from_markdown(str(final_md_out), final_cache_dir)
        builder.save(final_docx_out)

        logger.info(f"Done! Document compiled successfully: {final_docx_out}")
    except Exception as e:
        logger.error(f"Compile failed: {e}", exc_info=True)
        sys.exit(1)


@cli.command(name="list-templates")
def list_templates():
    """Lists all available templates in the templates directory."""
    templates_dir = BASE_DIR / "templates"
    manager = TemplateManager(templates_dir)
    templates = manager.list_templates()

    if not templates:
        logger.info("No templates found in templates directory.")
        return

    logger.info(f"Found {len(templates)} templates:")
    for template_id, config in templates.items():
        click.echo(f" -  {click.style(template_id, fg='green', bold=True)}")
        click.echo(f"    Name: {config.name}")
        click.echo(f"    Type: {config.type}")
        click.echo(f"    Desc: {config.description}")
        click.echo("")


@cli.command(name="create")
@click.argument("name")
@click.option("--template", required=True, help="Template ID/Name to base the project on.")
def create_workspace(name: str, template: str):
    """Creates a new workspace folder based on a template."""
    templates_dir = BASE_DIR / "templates"
    workspaces_dir = BASE_DIR / "workspaces"

    manager = TemplateManager(templates_dir)
    dest_dir = workspaces_dir / name

    if dest_dir.exists():
        logger.error(f"Workspace directory already exists: {dest_dir}")
        sys.exit(1)

    try:
        logger.info(f"Creating project '{name}' from template '{template}'...")
        manager.create_project(template, dest_dir)
        logger.info(f"Successfully created workspace at: {dest_dir}")
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
