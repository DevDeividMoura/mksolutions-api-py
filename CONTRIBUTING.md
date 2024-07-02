
# Contributing

Thank you for being interested in contributing to this SDK Python for MK Solutions API.
There are many ways you can contribute to the project:

- Try this SDK and [report bugs/issues you find](https://github.com/DevDeividMoura/mksolutions-api-py/issues/new)
- [Implement new features](https://github.com/DevDeividMoura/mksolutions-api-py/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
- [Review Pull Requests of others](https://github.com/DevDeividMoura/mksolutions-api-py/pulls)
- Write documentation
- Participate in discussions

## Reporting Bugs or Other Issues

Found something that this SDK should support?
Stumbled upon some unexpected behaviour?

Contributions should generally start out with [a discussion](https://github.com/DevDeividMoura/mksolutions-api-py/discussions).
Possible bugs may be raised as a "Potential Issue" discussion, feature requests may
be raised as an "Ideas" discussion. We can then determine if the discussion needs
to be escalated into an "Issue" or not, or if we'd consider a pull request.

Try to be more descriptive as you can and in case of a bug report,
provide as much information as possible like:

- OS platform
- Python version
- Installed dependencies and versions (`python -m pip freeze`)
- Code snippet
- Error traceback

You should always try to reduce any examples to the *simplest possible case*
that demonstrates the issue.

Some possibly useful tips for narrowing down potential issues...

- Does the issue exist with `MKSolutions`, `AsyncMKSolutions`, or both?
- When using `AsyncMKSolutions` does the issue exist when using `asyncio` or `trio`, or both?

## Development

To start developing this SDK create a **fork** of the
[MKSolutions API Python repository](https://github.com/DevDeividMoura/mksolutions-api-py) on GitHub.

Then clone your fork with the following command replacing `YOUR-USERNAME` with
your GitHub username:

```shell
git clone https://github.com/YOUR-USERNAME/mksolutions-api-py
```

## Setting up the environment

### On devcontainer

You can open this page in the dev container. The Dockerfile contains the Python image, will install Node.js 20.x, Prism, and Rye, and you will have everything you need to start coding.

### With Rye

We use [Rye](https://rye-up.com/) to manage dependencies so we highly recommend [installing it](https://rye-up.com/guide/installation/) as it will automatically provision a Python environment with the expected Python version.

After installing Rye, you'll just have to run this command:

```sh
$ rye sync --all-features
```

You can then run scripts using `rye run python script.py` or by activating the virtual environment:

```sh
$ rye shell
# or manually activate - https://docs.python.org/3/library/venv.html#how-venvs-work
$ source .venv/bin/activate

# now you can omit the `rye run` prefix
$ python script.py
```

### Without Rye

Alternatively, if you don't want to install `Rye`, you can stick with the standard `pip` setup by ensuring you have the Python version specified in `.python-version`, create a virtual environment however you desire, and then install dependencies using this command:

```sh
$ pip install -r requirements-dev.lock
```

## Testing, Linting, and Formatting

We use custom shell scripts to automate testing, linting, and documentation building workflow.

!!! Most tests require you to [set up a mock server](https://github.com/stoplightio/prism) against the OpenAPI spec to run the tests.

To run the tests, use:

```shell
scripts/test
```

!!! warning
    The test suite spawns testing servers on port **4010**.
    Make sure these are not in use, so the tests can run properly.

Any additional arguments will be passed to `pytest`. See the [pytest documentation](https://docs.pytest.org/en/latest/how-to/usage.html) for more information.

For example, to run a single test script:

First run the mock server if necessary:

```bash
# you will need npm installed
npx prism mock mks-api-spec/openapi.yaml
```

Then run the pytest command with options:

```shell
rye run pytest tests/test_client.py
```

This repository uses [ruff](https://github.com/astral-sh/ruff) and [black](https://github.com/psf/black) to format the code in the repository.

To lint:

```bash
rye run lint 
#or
scripts/lint
```

To format and fix all ruff issues automatically:

```bash
rye run format
#or
scripts/format
```

## Documenting

The types and methods of each module in this project should be documented in the `api.md` file.


## Publishing and Releases

Changes made to this repository via the automated release PR pipeline should publish to PyPI automatically. If the changes aren't made through the automated pipeline, you may want to make releases manually.

### Publish with a GitHub Workflow

You can release to package managers by using [the `Publish PyPI` GitHub action](https://www.github.com/openai/openai-python/actions/workflows/publish-pypi.yml). This requires a setup organization or repository secret to be set up.

### Publish Manually

If you need to manually release a package, you can run the `bin/publish-pypi` script with a `PYPI_TOKEN` set on the environment.
