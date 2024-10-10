import hashlib
import os


def _generate_filename() -> str:
    """Generate a filename."""
    return hashlib.md5(os.urandom(32)).hexdigest() + ".txt"


def save(data: str, file: str | None = None) -> None:
    """Save data to a file."""
    if file is None:
        file = _generate_filename()

    with open(file, "w") as f:
        f.write(data)


def merge(files: list[str], output: str) -> None:
    """Merge files into a single file."""
    with open(output, "w") as f:
        for file in files:
            with open(file) as src:
                f.write(src.read())
            os.remove(file)
