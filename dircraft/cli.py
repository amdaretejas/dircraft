import argparse
import sys
from pathlib import Path

from .creator import DirectoryCreator
from .templates import SUPPORTED_LANGUAGES, SUPPORTED_TYPES, get_template

DEFAULT_LANG = "python"
DEFAULT_NAME = "project"
DEFAULT_TYPE = "dev"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="dircraft",
        description="Scaffold a production-ready project folder structure.",
    )
    parser.add_argument(
        "pos_lang", nargs="?", default=None, help="Language (default: python)"
    )
    parser.add_argument(
        "pos_name", nargs="?", default=None, help="Folder name (default: project)"
    )
    parser.add_argument(
        "pos_type", nargs="?", default=None, help="Project type (default: dev)"
    )
    parser.add_argument("--lang", dest="lang", default=None, help="Language to scaffold for")
    parser.add_argument("--name", dest="name", default=None, help="Name of the folder to create")
    parser.add_argument("--type", dest="type", default=None, help="Project type, e.g. dev")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Write into the target folder even if it already exists and is not empty",
    )

    args = parser.parse_args(argv)

    lang = (args.lang or args.pos_lang or DEFAULT_LANG).lower()
    name = args.name or args.pos_name or DEFAULT_NAME
    type_ = (args.type or args.pos_type or DEFAULT_TYPE).lower()

    return lang, name, type_, args.force


def main(argv=None) -> int:
    lang, name, type_, force = parse_args(argv)

    if lang not in SUPPORTED_LANGUAGES:
        print(f"Unsupported language '{lang}'. Supported: {', '.join(sorted(SUPPORTED_LANGUAGES))}")
        return 1

    if type_ not in SUPPORTED_TYPES:
        print(f"Unsupported type '{type_}'. Supported: {', '.join(sorted(SUPPORTED_TYPES))}")
        return 1

    target = Path.cwd() / name
    if target.exists() and any(target.iterdir()) and not force:
        print(f"'{target}' already exists and is not empty. Use --force to write into it anyway.")
        return 1

    builder = get_template(lang, type_)
    structure = builder(name)

    DirectoryCreator(base_path=".").create(structure)

    print(f"Created '{name}' ({lang}/{type_}) project structure at {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
