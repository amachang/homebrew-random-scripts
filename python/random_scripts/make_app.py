import click
from pathlib import Path
import re
import jinja2
import os
import subprocess
from typing import Optional
import shlex

@click.command
@click.option("--file", "-f", "shell_script_path", type=Path, required=False, help="shell script file path")
@click.option("--command", "-c", "command", type=str, required=False, help="shell script source code")
@click.option("--app", "-a", "app_path", type=Path, required=True, help="app export path")
@click.option("--droppable-file", "-d", "droppable", is_flag=True, default=False, required=True, help="make app drag-n-dragg-able")
@click.option("--override", is_flag=True, show_default=True, default=False, help="allow override the current app file")
def main(shell_script_path: Optional[Path], command: Optional[str], app_path: Path, droppable: bool, override: bool) -> None:
    if command and shell_script_path:
        print("Error: Not allowed to give either --file and --command")
        exit(1)

    if not command and not shell_script_path:
        print("Error: --file or --command must specify either")
        exit(1)

    if shell_script_path:
        command = shlex.join(['source', str(shell_script_path.absolute())])

    assert isinstance(command, str)

    filename = app_path.name
    if match := re.fullmatch(r"(.*?)\.app", filename):
        basename = match.group(1)
    else:
        basename = filename
        filename = basename + ".app"
        app_path = output_dir.joinpath(filename)

    output_dir = app_path.parent
    if not override and app_path.exists():
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

