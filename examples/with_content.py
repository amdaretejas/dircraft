from dircraft import DirectoryCreator

paths = {
    "project_root/src/main.py": "# FastAPI entry\n",
    "project_root/README.md": "# My Project\n",
    "project_root/tests": None
}

DirectoryCreator().create(paths)
print("✅ Structure + files created")
