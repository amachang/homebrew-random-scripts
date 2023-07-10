import click
from pathlib import Path
import re
import jinja2
import os
import subprocess

@click.command
@click.argument("command", type=str, required=True)
@click.argument("app_path", type=Path, required=True)
@click.option("--mode", '-m', type=click.Choice(['accept_file', 'just_run']), required=True, help="'accept_file' if you accept the path of the drag-n-drop-ed file as the last command line argument")
def main(command: str, app_path: Path, mode: str) -> None:
    """
    The script make an app bundle for macOS\n
    Example: make_app -m accept_file 'open -n -a VLC' ~/Desktop/NewVLCWindow.app
    """
    droppable = mode == 'accept_file'

    filename = app_path.name
    if match := re.fullmatch(r"(.*?)\.app", filename):
        basename = match.group(1)
    else:
        basename = filename
        filename = basename + ".app"
        app_path = output_dir.joinpath(filename)

    output_dir = app_path.parent
    if app_path.exists():
        print("Error: file exists in", app_path)
        exit(1)

    main_script_filename = basename + ".applescript"
    main_script_path = output_dir.joinpath(main_script_filename)

    output_dir.mkdir(parents=True, exist_ok=True)

    template_dir = Path(__file__).absolute().parent.parent.joinpath("res", "make_app")
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=False,
    )
    main_script_template = template_env.get_template("main.applescript")

    command = re.sub(r'\\', '\\\\\\\\', command)
    command = re.sub(r'"', '\\"', command)

    main_script = main_script_template.render({
        "droppable": droppable,
        "command": command,
    })
    main_script_path.write_text(main_script)

    subprocess.check_call(['osacompile', '-o', app_path, main_script_path])
    print("Done:", app_path)

if __name__ == "__main__":
    main()

