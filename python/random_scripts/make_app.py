import click
from pathlib import Path
import re
import jinja2
import os
import subprocess

@click.command
@click.argument("command", type=str, required=True)
@click.argument("output_path", type=Path, required=True)
def main(command: str, output_path: Path) -> None:
    filename = output_path.name
    if match := re.fullmatch(r"(.*?)\.app", filename):
        basename = match.group(1)
    else:
        basename = filename
        filename = basename + ".app"
        output_path = output_dir.joinpath(filename)

    output_dir = output_path.parent
    if output_path.exists():
        print("Error: file exists in", output_path)
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
    main_script = main_script_template.render({"command": command})
    main_script_path.write_text(main_script)

    subprocess.check_call(['osacompile', '-o', output_path, main_script_path])
    print("Done:", output_path)

if __name__ == "__main__":
    main()

