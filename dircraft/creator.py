from pathlib import Path
from typing import List, Dict, Union


class DirectoryCreator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)

    def create(self, paths: Union[List[str], Dict[str, str]]) -> None:
        """
        Create folders and files.

        - List[str] → auto detect files/folders
        - Dict[path, content] → file with content or folder if content is None
        """
        if isinstance(paths, list):
            self._create_from_list(paths)
        elif isinstance(paths, dict):
            self._create_from_dict(paths)
        else:
            raise TypeError("paths must be list or dict")

    def _create_from_list(self, paths: List[str]):
        for path in paths:
            full_path = self.base_path / path

            if full_path.suffix:  # file
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.touch(exist_ok=True)
            else:  # directory
                full_path.mkdir(parents=True, exist_ok=True)

    def _create_from_dict(self, paths: Dict[str, Union[str, None]]):
        for path, content in paths.items():
            full_path = self.base_path / path

            if content is None:
                full_path.mkdir(parents=True, exist_ok=True)
            else:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
