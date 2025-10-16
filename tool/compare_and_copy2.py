from __future__ import annotations

import shutil
from pathlib import Path

REPO_DIR = Path(r"G:\repogitory\deep-sengoku.souten\hime")
RELEASE_DIR = Path(r"R:\Release\蒼天録\女")
DEST_DIR = Path(r"G:\dst")


def part_before_first_dot(name: str) -> str:
    """Return the substring before the first dot in the filename."""
    head, _, _ = name.partition(".")
    return head


def collect_repo_filenames(repo_dir: Path) -> list[str]:
    """Collect all filenames (casefolded) from the repository directory."""
    filenames: list[str] = []
    for path in repo_dir.rglob("*"):
        if path.is_file():
            filenames.append(path.name.casefold())
    return filenames


def main() -> None:
    if not REPO_DIR.is_dir():
        raise FileNotFoundError(f"Repository directory not found: {REPO_DIR}")

    if not RELEASE_DIR.is_dir():
        raise FileNotFoundError(f"Release directory not found: {RELEASE_DIR}")

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    repo_names = collect_repo_filenames(REPO_DIR)
    copied_files: list[tuple[Path, Path]] = []

    for release_file in RELEASE_DIR.rglob("*"):
        if not release_file.is_file():
            continue

        base_name = part_before_first_dot(release_file.name).casefold()
        has_match = any(base_name in repo_name for repo_name in repo_names)

        if has_match:
            continue

        relative_path = release_file.relative_to(RELEASE_DIR)
        destination = DEST_DIR / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():
            print(f"Skip (already exists): {destination}")
            continue

        shutil.copy2(release_file, destination)
        copied_files.append((release_file, destination))
        print(f"Copied: {release_file} -> {destination}")

    print(f"Copied {len(copied_files)} file(s) to {DEST_DIR}.")


if __name__ == "__main__":
    main()