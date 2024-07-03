# About this template

Hi, I created this template to help you get started with a new project.

I have created and maintained a number of python libraries, applications and 
frameworks and during those years I have learned a lot about how to create a 
project structure and how to structure a project to be as modular and simple 
as possible.

Some decisions I have made while creating this template are:

 - Create a project structure that is as modular as possible.
 - Keep it simple and easy to maintain.
 - Allow for a lot of flexibility and customizability.
 - Low dependency (this template doesn't add dependencies)

## Structure

Lets take a look at the structure of this template:

```text
├── Containerfile            # The file to build a container using buildah or docker
├── CONTRIBUTING.md          # Onboarding instructions for new contributors
├── docs                     # Documentation site (add more .md files here)
│   └── index.md             # The index page for the docs site
├── .github                  # Github metadata for repository
│   ├── release_message.sh   # A script to generate a release message
│   └── workflows            # The CI pipeline for Github Actions
├── .gitignore               # A list of files to ignore when pushing to Github
├── HISTORY.md               # Auto generated list of changes to the project
├── LICENSE                  # The license for the project
├── Makefile                 # A collection of utilities to manage the project
├── MANIFEST.in              # A list of files to include in a package
├── mkdocs.yml               # Configuration for documentation site
├── neptun_webscraper             # The main python package for the project
│   ├── base.py              # The base module for the project
│   ├── __init__.py          # This tells Python that this is a package
│   ├── __main__.py          # The entry point for the project
│   └── VERSION              # The version for the project is kept in a static file
├── README.md                # The main readme for the project
├── setup.py                 # The setup.py file for installing and packaging the project
├── requirements.txt         # An empty file to hold the requirements for the project
├── requirements-test.txt    # List of requirements for testing and devlopment
├── setup.py                 # The setup.py file for installing and packaging the project
└── tests                    # Unit tests for the project (add mote tests files here)
    ├── conftest.py          # Configuration, hooks and fixtures for pytest
    ├── __init__.py          # This tells Python that this is a test package
    └── test_base.py         # The base test case for the project
```

## FAQ

Frequent asked questions.

### Why this template is not using [Poetry](https://python-poetry.org/) ?

I really like Poetry and I think it is a great tool to manage your python projects,
if you want to switch to poetry, you can run `make switch-to-poetry`.

But for this template I wanted to keep it simple.

Setuptools is the most simple and well supported way of packaging a Python project,
it doesn't require extra dependencies and is the easiest way to install the project.

Also, poetry doesn't have a good support for installing projects in development mode yet.

### Why the `requirements.txt` is empty ?

This template is a low dependency project, so it doesn't have any extra dependencies.
You can add new dependencies as you will or you can use the `make init` command to
generate a `requirements.txt` file based on the template you choose `flask, fastapi, click etc`.

### Why there is a `requirements-test.txt` file ?

This file lists all the requirements for testing and development,
I think the development environment and testing environment should be as similar as possible.

Except those tools that are up to the developer choice (like ipython, ipdb etc).

### Why the template doesn't have a `pyproject.toml` file ?

It is possible to run `pip install https://github.com/name/repo/tarball/main` and
have pip to download the package direcly from Git repo.

For that to work you need to have a `setup.py` file, and `pyproject.toml` is not
supported for that kind of installation.

I think it is easier for example you want to install specific branch or tag you can
do `pip install https://github.com/name/repo/tarball/{TAG|REVISON|COMMIT}`

People automating CI for your project will be grateful for having a setup.py file

### Why isn't this template made as a cookiecutter template?

I really like [cookiecutter](https://github.com/cookiecutter/cookiecutter) and it is a great way to create new projects,
but for this template I wanted to use the Github `Use this template` button,
to use this template doesn't require to install extra tooling such as cookiecutter.

Just click on [Use this template](https://github.com/rochacbruno/python-project-template/generate) and you are good to go.

The substituions are done using github actions and a simple sed script.

### Why `VERSION` is kept in a static plain text file?

I used to have my version inside my main module in a `__version__` variable, then
I had to do some tricks to read that version variable inside the setuptools 
`setup.py` file because that would be available only after the installation.

I decided to keep the version in a static file because it is easier to read from
wherever I want without the need to install the package.

e.g: `cat neptun_webscraper/VERSION` will get the project version without harming
with module imports or anything else, it is useful for CI, logs and debugging.

### Why to include `tests`, `history` and `Containerfile` as part of the release?

The `MANIFEST.in` file is used to include the files in the release, once the 
project is released to PyPI all the files listed on MANIFEST.in will be included
even if the files are static or not related to Python.

Some build systems such as RPM, DEB, AUR for some Linux distributions, and also
internal repackaging systems tends to run the tests before the packaging is performed.

The Containerfile can be useful to provide a safer execution environment for 
the project when running on a testing environment.

I added those files to make it easier for packaging in different formats.

### Why conftest includes a go_to_tmpdir fixture?

When your project deals with file system operations, it is a good idea to use
a fixture to create a temporary directory and then remove it after the test.

Before executing each test pytest will create a temporary directory and will
change the working directory to that path and run the test.

So the test can create temporary artifacts isolated from other tests.

After the execution Pytest will remove the temporary directory.

### Why this template is not using [pre-commit](https://pre-commit.com/) ?

pre-commit is an excellent tool to automate checks and formatting on your code.

However I figured out that pre-commit adds extra dependency and it an entry barrier
for new contributors.

Having the linting, checks and formatting as simple commands on the [Makefile](Makefile)
makes it easier to undestand and change.

Once the project is bigger and complex, having pre-commit as a dependency can be a good idea.

### Why the CLI is not using click?

I wanted to provide a simple template for a CLI application on the project main entry point
click and typer are great alternatives but are external dependencies and this template
doesn't add dependencies besides those used for development.

### Why this doesn't provide a full example of application using Flask or Django?

as I said before, I want it to be simple and multipurpose, so I decided to not include
external dependencies and programming design decisions.

It is up to you to decide if you want to use Flask or Django and to create your application
the way you think is best.

This template provides utilities in the Makefile to make it easier to you can run:

```bash
$ make init 
Which template do you want to apply? [flask, fastapi, click, typer]? > flask
Generating a new project with Flask ...
```

Then the above will download the Flask template and apply it to the project.

## The Makefile

All the utilities for the template and project are on the Makefile

```bash
❯ make
Usage: make <target>

Targets:
help:             ## Show the help.
install:          ## Install the project in dev mode.
fmt:              ## Format code using black & isort.
lint:             ## Run pep8, black, mypy linters.
test: lint        ## Run tests and generate coverage report.
watch:            ## Run tests on every change.
clean:            ## Clean unused files.
virtualenv:       ## Create a virtual environment.
release:          ## Create a new tag for release.
docs:             ## Build the documentation.
switch-to-poetry: ## Switch to poetry package manager.
init:             ## Initialize the project based on an application template.
```

## README - Python Project Template

A low dependency and really simple to start project template for Python Projects.

See also 
- [Flask-Project-Template](https://github.com/rochacbruno/flask-project-template/) for a full feature Flask project including database, API, admin interface, etc.
- [FastAPI-Project-Template](https://github.com/rochacbruno/fastapi-project-template/) The base to start an openapi project featuring: SQLModel, Typer, FastAPI, JWT Token Auth, Interactive Shell, Management Commands.

### HOW TO USE THIS TEMPLATE

> **DO NOT FORK** this is meant to be used from **[Use this template](https://github.com/rochacbruno/python-project-template/generate)** feature.

1. Click on **[Use this template](https://github.com/rochacbruno/python-project-template/generate)**
3. Give a name to your project  
   (e.g. `my_awesome_project` recommendation is to use all lowercase and underscores separation for repo names.)
3. Wait until the first run of CI finishes  
   (Github Actions will process the template and commit to your new repo)
4. If you want [codecov](https://about.codecov.io/sign-up/) Reports and Automatic Release to [PyPI](https://pypi.org)  
  On the new repository `settings->secrets` add your `PYPI_API_TOKEN` and `CODECOV_TOKEN` (get the tokens on respective websites)
4. Read the file [CONTRIBUTING.md](CONTRIBUTING.md)
5. Then clone your new project and happy coding!

> **NOTE**: **WAIT** until first CI run on github actions before cloning your new project.

### What is included on this template?

- 🖼️ Templates for starting multiple application types:
  * **Basic low dependency** Python program (default) [use this template](https://github.com/rochacbruno/python-project-template/generate)
  * **Flask** with database, admin interface, restapi and authentication [use this template](https://github.com/rochacbruno/flask-project-template/generate).
  **or Run `make init` after cloning to generate a new project based on a template.**
- 📦 A basic [setup.py](setup.py) file to provide installation, packaging and distribution for your project.  
  Template uses setuptools because it's the de-facto standard for Python packages, you can run `make switch-to-poetry` later if you want.
- 🤖 A [Makefile](Makefile) with the most useful commands to install, test, lint, format and release your project.
- 📃 Documentation structure using [mkdocs](http://www.mkdocs.org)
- 💬 Auto generation of change log using **gitchangelog** to keep a HISTORY.md file automatically based on your commit history on every release.
- 🐋 A simple [Containerfile](Containerfile) to build a container image for your project.  
  `Containerfile` is a more open standard for building container images than Dockerfile, you can use buildah or docker with this file.
- 🧪 Testing structure using [pytest](https://docs.pytest.org/en/latest/)
- ✅ Code linting using [flake8](https://flake8.pycqa.org/en/latest/)
- 📊 Code coverage reports using [codecov](https://about.codecov.io/sign-up/)
- 🛳️ Automatic release to [PyPI](https://pypi.org) using [twine](https://twine.readthedocs.io/en/latest/) and github actions.
- 🎯 Entry points to execute your program using `python -m <neptun_webscraper>` or `$ neptun_webscraper` with basic CLI argument parsing.
- 🔄 Continuous integration using [Github Actions](.github/workflows/) with jobs to lint, test and release your project on Linux, Mac and Windows environments.

> Curious about architectural decisions on this template? read [ABOUT_THIS_TEMPLATE.md](ABOUT_THIS_TEMPLATE.md)  
> If you want to contribute to this template please open an [issue](https://github.com/rochacbruno/python-project-template/issues) or fork and send a PULL REQUEST.

[❤️ Sponsor this project](https://github.com/sponsors/rochacbruno/)
