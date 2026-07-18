```
       ___                      ______
  ____/ (_)__________________ _/ __/ /_
 / __  / / ___/ ___/ ___/ __ `/ /_/ __/
/ /_/ / / /  / /__/ /  / /_/ / __/ /_
\__,_/_/_/   \___/_/   \__,_/_/  \__/
```

<p>
  <a href="https://pypi.org/project/pydircraft/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pydircraft.svg"></a>
  <a href="https://pypi.org/project/pydircraft/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/pydircraft.svg"></a>
  <a href="https://github.com/amdaretejas/dircraft/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg"></a>
</p>

Scaffold production-ready project folder structures — from the CLI or from Python.

## Install

```bash
pip install pydircraft
# or
uv add pydircraft
```

This installs the `dircraft` command and the `dircraft` Python package.

## CLI usage

Once installed, the `dircraft` command is available on your PATH:

```bash
# explicit flags
dircraft --lang python --name agent --type dev

# positional shorthand — same result
dircraft python agent dev

# no args at all → defaults to python / project / dev
dircraft

# only override what you need
dircraft --name myapp

# re-run into a folder that already has files in it
dircraft python agent dev --force
```

| Flag                | Default   | Meaning                              |
|---------------------|-----------|---------------------------------------|
| `--lang` / 1st arg   | `python`  | Language to scaffold for              |
| `--name` / 2nd arg   | `project` | Name of the folder to create          |
| `--type` / 3rd arg   | `dev`     | Project type                          |
| `--force`            | off       | Overwrite a non-empty target folder   |

Currently supported: `--lang python --type dev`, which creates a full-stack
development scaffold **in the directory the command is run from**:

```
<name>/
├── backend/            # FastAPI app (app/, tests/, scripts/, Dockerfile, requirements.txt)
├── frontend/           # Streamlit app (main.py, pages/, services/, Dockerfile, requirements.txt)
├── .gitignore
├── .env / .env.example
├── .editorconfig
├── docker-compose.yml
└── README.md
```

Run it:

```bash
cd agent/backend && pip install -r requirements.txt && uvicorn app.main:app --reload
cd agent/frontend && pip install -r requirements.txt && streamlit run main.py
# or, with Docker
cd agent && docker-compose up --build
```

More `--lang` / `--type` combinations will be added over time.

## Library usage

`DirectoryCreator` also works standalone, from a plain list of paths:

```python
from dircraft import DirectoryCreator

folder_paths = [
    "project_root/src",
    "project_root/tests",
    "project_root/docs",
    "project_root/assets/images",
    "project_root/assets/styles",
]

DirectoryCreator().create(folder_paths)
print("✅ Folder structure created successfully")
```

Anything with a file extension is created as a file, everything else as a
directory.

Or from a `dict` of `path -> content`, when you want files pre-filled
(`None` for a plain directory):

```python
from dircraft import DirectoryCreator

paths = {
    "project_root/src/main.py": "# FastAPI entry\n",
    "project_root/README.md": "# My Project\n",
    "project_root/tests": None,
}

DirectoryCreator().create(paths)
print("✅ Structure + files created")
```

More examples in [`examples/`](examples/).

## License

Apache License 2.0 — see [LICENSE](LICENSE).
