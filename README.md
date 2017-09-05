ZEF: The project planning tool (assuming you're using Github + Zenhub)

## Getting started

Create a virtual environment and install the dependencies
```bash
$ virtualenv venv --python=python3
$ . venv/bin/active
$ pip install requirements.txt
```

pip 'install' the package (until it's officially on pypi)
```bash
$ pip install --editable .
```

From there the `zef` command should be in your PATH so you can run
```bash
$ zef --help
$ zef points --milestone web-128 --assignee gkadillak --labels interrupt
```
