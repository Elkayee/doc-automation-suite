import sys
import json
from pathlib import Path
import click

# Ensure the root directory of the workspace is in the python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.logger import logger
from src.core.export import compile_document
from src.core.batch import load_batch_manifest, run_batch
from src.core.file_io import atomic_write
from src.core.project_paths import workspace_path
from src.core.renderers import renderer_status
from src.core.template_manager import TemplateManager
from src.core.runtime import VERSION, data_root, resource_root

BASE_DIR = resource_root()


@click.group()
@click.version_option(version=VERSION)
def cli():
    """Doc Automation Suite CLI toolkit."""
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')


@cli.command(name="compile")
@click.argument("workspace_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--docx-out", type=click.Path(path_type=Path), help="Custom path for the compiled DOCX file.")
@click.option("--md-out", type=click.Path(path_type=Path), help="Custom path for the assembled Markdown file.")
@click.option("--cache-dir", type=click.Path(path_type=Path), help="Custom path for rendering image cache.")
@click.option('--pdf-out', type=click.Path(path_type=Path), help='PDF output path.')
@click.option('--format', 'formats', multiple=True, type=click.Choice(['docx', 'pdf']), default=['docx'])
@click.option('--final/--draft', 'final', default=False, help='Reject incomplete content and update fields for a final export.')
@click.option('--engine', type=click.Choice(['auto', 'builtin', 'academic']), default='auto')
@click.option('--metadata', 'metadata_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--json', 'as_json', is_flag=True, help='Print the structured export result.')
def compile_workspace(workspace_dir: Path, docx_out: Path, md_out: Path, cache_dir: Path,
                      pdf_out, formats, final, engine, metadata_file, as_json):
    """Assembles and compiles a markdown workspace into a Word document."""
    try:
        metadata = json.loads(metadata_file.read_text(encoding='utf-8')) if metadata_file else None
        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError('Metadata must be a JSON object')
        result = compile_document(workspace_dir, docx_out=docx_out, md_out=md_out, pdf_out=pdf_out,
                                  formats=formats, mode='final' if final else 'draft', engine=engine,
                                  cache_dir=cache_dir, metadata=metadata)
        if as_json:
            click.echo(json.dumps(result.to_dict(), ensure_ascii=False))
        else:
            click.echo(f'DOCX: {result.compiled_docx}')
            if result.compiled_pdf:
                click.echo(f'PDF: {result.compiled_pdf}')
            for warning in result.warnings:
                click.echo(f'Cảnh báo: {warning}', err=True)
    except Exception as e:
        if as_json:
            click.echo(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))
            raise click.exceptions.Exit(1)
        raise click.ClickException(str(e)) from e


@cli.command(name='batch')
@click.argument('manifest', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--result-out', type=click.Path(path_type=Path), help='JSON results for every item.')
def batch_export(manifest, result_out):
    """Export a JSON/YAML manifest or CSV/XLSX metadata rows sequentially."""
    try:
        jobs = load_batch_manifest(manifest)
        result = run_batch(jobs, base_dir=manifest.resolve().parent, templates_dir=BASE_DIR / 'templates')
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if result_out:
        atomic_write(result_out, text)
    click.echo(text)
    if not result['success']:
        raise click.exceptions.Exit(1)


@cli.command(name='doctor')
def doctor():
    """Show locally available PDF and academic renderers."""
    click.echo(json.dumps(renderer_status(), ensure_ascii=False, indent=2))


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
    workspaces_dir = data_root(BASE_DIR) / "workspaces"

    manager = TemplateManager(templates_dir)
    try:
        dest_dir = workspace_path(workspaces_dir, name)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

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
