# from dircraft import DirectoryCreator
from dircraft import DirectoryCreator

paths = [
    "project_root/src",
    "project_root/src/main.py",
    "project_root/src/config/settings.py",
    "project_root/tests",
    "project_root/tests/test_main.py",
    "project_root/README.md"
]

DirectoryCreator().create(paths)
print("✅ Structure created")
