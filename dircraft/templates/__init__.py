from typing import Callable, Dict, Optional, Set, Tuple

from .python_dev import build_python_dev_structure

TemplateBuilder = Callable[[str], Dict[str, Optional[str]]]

_REGISTRY: Dict[Tuple[str, str], TemplateBuilder] = {
    ("python", "dev"): build_python_dev_structure,
}

SUPPORTED_LANGUAGES: Set[str] = {lang for lang, _ in _REGISTRY}
SUPPORTED_TYPES: Set[str] = {type_ for _, type_ in _REGISTRY}


def get_template(lang: str, type_: str) -> TemplateBuilder:
    return _REGISTRY[(lang, type_)]
