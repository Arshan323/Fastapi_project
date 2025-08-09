import click
import shutil
from pathlib import Path
import importlib.resources as pkg_resources

@click.group()
def cli():
    pass

@cli.command()
@click.argument("name")
def init(name):
    """Create new API project."""
    dest_path = Path(name)
    if dest_path.exists():
        click.echo("❌ Folder already exists!")
        return
    
    with pkg_resources.path("my_module", "templates") as template_dir:
        shutil.copytree(template_dir, dest_path)
    
    click.echo(f"✅ Project '{name}' created.")

if __name__ == "__main__":
    cli()
