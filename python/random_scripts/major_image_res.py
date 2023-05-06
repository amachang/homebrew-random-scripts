import imagesize
import click
from collections import Counter
from pathlib import Path
from typing import List, Tuple, Optional, cast
from tqdm import tqdm


@click.command
@click.argument("gallery_dirs", nargs=-1, type=Path, required=True)
@click.option("-n", "--num-results", "result_count", type=int, default=3, required=False)
def main(gallery_dirs: List[Path], result_count: int) -> None:
    gallery_major_resolutions: List[Tuple[Path, List[Tuple[Tuple[int, int], int]]]] = []
    for gallery_dir in gallery_dirs:
        if not gallery_dir.is_dir():
            continue

        resolutions = get_resolutions_in_dir(gallery_dir)
        if len(resolutions) == 0:
            continue

        resolution_counter = Counter(resolutions)
        major_resolutions = cast(List[Tuple[Tuple[int, int], int]], resolution_counter.most_common(result_count))
        gallery_major_resolutions.append((gallery_dir, major_resolutions))

    gallery_major_resolutions = sorted(gallery_major_resolutions, key=lambda el: -max(el[1][0][0]))

    for gallery_dir, major_resolutions in gallery_major_resolutions:
        print(f"{gallery_dir}")
        for index, ((width, height), image_count) in enumerate(major_resolutions):
            print(f"    {index+1}: {width}x{height} ({image_count} images)")


def get_resolutions_in_dir(image_dir: Path) -> List[Tuple[int, int]]:
    assert image_dir.is_dir()
    resolutions = []
    pbar = tqdm(image_dir.iterdir())
    pbar.set_description(f"Walking {image_dir.name}")
    for image_file_path in pbar:
        if image_file_path.is_dir():
            resolutions.extend(get_resolutions_in_dir(image_file_path))
        else:
            try:
                resolution = cast(Tuple[int, int], imagesize.get(image_file_path))
            except:
                continue
            width, height = resolution
            if width == -1 or height == -1:
                continue
            resolutions.append(resolution)
    return resolutions


if __name__ == "__main__":
    main()

