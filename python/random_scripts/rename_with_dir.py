import os
import shutil
from os import path
import re
from pathlib import Path
from argparse import ArgumentParser
from typing import Any, List, Set
import logging

logging.basicConfig(level=logging.DEBUG)

ignore_target_filenames = {
    '.DS_Store',
    'desktop.ini',
    'Desktop.ini',
    'Thumbs.db',
};

def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--run", action="store_true")
    arg_parser.add_argument("regex", type=re.compile)
    arg_parser.add_argument("replacement", type=str)
    args = arg_parser.parse_args()

    dry_run: bool = not args.run
    regex: re.Pattern = args.regex
    replacement: str = args.replacement
    file_path_list = get_file_path_list()

    target_file_count = 0
    nontarget_file_count = 0
    new_file_path_list = []
    for file_path in file_path_list:
        new_file_path = regex.sub(replacement, file_path)
        if file_path != new_file_path:
            dir_list = reversed(Path(new_file_path).parents)
            for d in dir_list:
                if not exists_dir(d):
                    make_dir(d, dry_run)
            target_file_count += 1
        else:
            nontarget_file_count += 1
        new_file_path_list.append(new_file_path)

    possibly_empty_dirs = set()
    for file_path, new_file_path in zip(file_path_list, new_file_path_list):
        if file_path != new_file_path:
            move_file(file_path, new_file_path, dry_run)
            possibly_empty_dirs.add(path.dirname(file_path))
    
    for d in possibly_empty_dirs:
        subdirs = [Path(d)] + list(Path(d).parents)
        for subdir in subdirs:
            entry_list = os.listdir(subdir)
            ignore_target_entry_list = [entry for entry in entry_list if entry in ignore_target_filenames]
            non_ignore_target_entry_list = [entry for entry in entry_list if entry not in ignore_target_filenames]
            logging.info(f'Check dir empty {subdir}')
            if len(non_ignore_target_entry_list) == 0:
                if not dry_run:
                    logging.info(f'Remove empty dir {subdir}')
                    for entry in ignore_target_entry_list:
                        logging.info(f'Remove {entry}')
                        subdir.joinpath(entry).unlink()
                    subdir.rmdir()
            else:
                break

    print(f'Renamed {target_file_count} files.')
    print(f'Ignored {nontarget_file_count} files.')

def get_file_path_list(d: str = '.') -> List[str]:
    file_path_list = []
    for entryname in os.listdir(d):
        if d == '.':
            entry_path = entryname
        else:
            entry_path = path.join(d, entryname)

        if path.isdir(entry_path):
            file_path_list.extend(get_file_path_list(entry_path))
        else:
            if entryname in ignore_target_filenames:
                continue
            file_path_list.append(entry_path)
    return file_path_list

dry_maked_dirs: Set[Path] = set()

def exists_dir(d: Path) -> bool:
    global dry_maked_dirs
    return d.exists() or d in dry_maked_dirs

def make_dir(d: Path, dry_run: bool) -> None:
    global dry_maked_dirs
    if not d.is_dir():
        assert not d.exists()
        logging.info(f'Make dir {d}')
        if dry_run:
            dry_maked_dirs.add(d)
        else:
            d.mkdir()

dry_moved_file_paths: Set[str] = set()

def move_file(file_path: str, new_file_path: str, dry_run: bool) -> None:
    assert path.exists(file_path)
    if path.exists(new_file_path) or new_file_path in dry_moved_file_paths:
        raise FileExistsError(f'Error during rename {file_path}: {new_file_path} already exists, operation aborted')

    logging.info(f'Move from {file_path} to {new_file_path}')
    if dry_run:
        dry_moved_file_paths.add(new_file_path)
    else:
        shutil.move(file_path, new_file_path)

if __name__ == "__main__":
    main()

