# Algorithm Service

Here are all files responsible for The Algorithm, that is a combination of sentiment analysis, entity recognition and keyword/n-gram scanning of content.

## Installation

Initially, you need `python` 3.5.x or higher and `virtualenv` to be installed on your machine.

```bash
    # to keep the namespace clean
    virtualenv -p python3 .venv

    # to install dependencies
    pip install -r requirements.txt

    # enter the virtual environment
    source .venv/bin/activate

    # Also, due to the usage of SpaCy, you will need to download the language model
    # For more info about it, check the SpaCy docs
    python -m spacy download en
```

## Testing

Run `./runtests` script from terminal.
Tests are written using `unittest` package from standard library.

## Profiling

The current version of `./runprofile` script does not support command line arguments. To be modified in future. For now the `main.py` script requires substitution of all occurrences of command line arguments in the code. There's a comment there.

## Style Guide

Full PEP8 [here](https://www.python.org/dev/peps/pep-0008/) compliance. You may use PyLint. 1 tab must be 4 spaces wide. Don't use tab character. Configure your editor accordingly. Docstrings must follow NumPy/SciPy style [here](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt).

