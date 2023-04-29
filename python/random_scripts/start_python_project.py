from argparse import ArgumentParser
from os import path
from pathlib import Path
import click
import json
import keyring
import logging
from github import Github
from github.Repository import Repository
from appdirs import user_config_dir
import jinja2
import virtualenv
import subprocess

logging.basicConfig(level=logging.DEBUG)


def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("project_name", type=str)
    arg_parser.add_argument("-g", "--make_github_repo", action="store_true")
    arg_parser.add_argument(
        "-d",
        "--dev_root_dir",
        type=Path,
        default=Path(path.expanduser("~")).joinpath("dev"),
    )
    args = arg_parser.parse_args()

    project_name = args.project_name
    check_project_name(project_name)

    dev_root_dir = args.dev_root_dir
    project_dir = dev_root_dir.joinpath(project_name)
    project_dir.mkdir(parents=True, exist_ok=False)
    logging.debug(f"Creted the project directory: {project_dir}")

    project_src_dir = project_dir.joinpath(underscore_project_name(project_name))
    project_src_dir.mkdir(parents=True, exist_ok=False)
    project_src_dir.joinpath("__init__.py").touch()
    logging.debug(f"Creted the project source directory: {project_src_dir}")

    project_test_dir = project_dir.joinpath("tests")
    project_test_dir.mkdir(parents=True, exist_ok=False)
    project_test_dir.joinpath("__init__.py").touch()
    logging.debug(f"Creted the project test directory: {project_test_dir}")

    template_dir = Path(
        path.join(
            path.dirname(path.dirname(path.abspath(__file__))),
            "res",
            "start_python_project",
            "template",
        )
    )
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=False,
    )
    template_env.filters["underscore"] = underscore_project_name
    template_env.filters["to_headlinese"] = to_headlinese_project_name
    template_rendered_file_map = {
        "README.md": "README.md",
        "coveragerc": ".coveragerc",
        "gitignore": ".gitignore",
        "mypy.ini": "mypy.ini",
        "pytest.ini": "pytest.ini",
        "setup.py": "setup.py",
        "tox.ini": "tox.ini",
    }
    for template_name, rendered_filename in template_rendered_file_map.items():
        template = template_env.get_template(template_name)
        rendered_text = template.render({"project_name": project_name})
        rendered_file_path = project_dir.joinpath(rendered_filename)
        rendered_file_path.write_text(rendered_text)
        logging.debug(f"Creted file: {rendered_file_path}")

    if args.make_github_repo:
        github = prepare_github_api()
        user = github.get_user()
        repo = user.create_repo(project_name)
        logging.debug(f"Creted the repo: {repo}")
        commit_and_push_project_files(project_dir, repo)
        logging.debug(f"Pushed the project dir")

    venv_dir = project_dir.joinpath("venv")
    virtualenv.cli_run([str(venv_dir)])
    subprocess.run(
        [str(venv_dir.joinpath("bin", "pip")), "install", "-e", str(project_dir)]
    )


def check_project_name(project_name: str) -> None:
    raise NotImplementedError()


def underscore_project_name(project_name: str) -> str:
    raise NotImplementedError()


def to_headlinese_project_name(project_name: str) -> str:
    raise NotImplementedError()


def prepare_github_api() -> Github:
    github_username = get_github_username()
    # Access OS Keychain
    access_token = keyring.get_password("github.com", github_username)
    return Github(access_token)


def get_github_username() -> str:
    config_dir = Path(user_config_dir("start_python_project"))
    config_dir.mkdir(parents=True, exist_ok=True)
    config_json_path = config_dir.joinpath("config.json")
    if not config_json_path.exists():
        config_json_path.write_text("{}")
    config = json.loads(config_json_path.read_text())
    if "github_username" not in config:
        github_username = click.prompt("Please enter github username")
        check_github_username(github_username)
        config["github_username"] = github_username
        config_json_path.write_text(json.dumps(config))
    return config["github_username"]


def commit_and_push_project_files(project_dir: Path, repo: Repository) -> None:
    raise NotImplementedError()


def check_github_username(username: str) -> None:
    raise NotImplementedError()


if __name__ == "__main__":
    main()
