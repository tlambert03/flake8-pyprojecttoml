.. image:: https://gitlab.com/durko/flake8-pyprojecttoml/badges/master/pipeline.svg
   :target: https://gitlab.com/durko/flake8-pyprojecttoml/-/commits/master
   :alt: pipeline status

.. image:: https://gitlab.com/durko/flake8-pyprojecttoml/badges/master/coverage.svg
   :target: https://gitlab.com/durko/flake8-pyprojecttoml/-/commits/master
   :alt: coverage report


====================
flake8-pyprojecttoml
====================

This extension adds support reading flake8 config from **pyproject.toml**. It uses flake8's plugin system to automatically monkeypatch the config system. Settings from pyproject.toml will be used regardless of invocation (CLI, pytest, IDE, ...).


Getting started
===============

Simply install with pip::

   pip install flake8-pyprojecttoml


Migrate your flake8 config to pyproject.toml (`example <https://gitlab.com/durko/flake8-pyprojecttoml/-/blob/master/pyproject.toml>`_) and use as usual.


Contributing
============

Thank you for considering to contribute to flake8-pyprojecttoml.

To submit issues or create merge requests please follow the instructions provided in the `contribution guide <https://gitlab.com/durko/flake8-pyprojecttoml/-/blob/master/CONTRIBUTING.rst>`_.

By contributing to flake8-pyprojecttoml you accept and agree to the terms and conditions laid out in there.


Development
===========

Clone the repository and setup your local checkout::

   git clone https://gitlab.com/durko/flake8-pyprojecttoml.git
   
   cd flake8-pyprojecttoml
   python -m venv venv
   . venv/bin/activate
   
   pip install -r requirements-dev.txt
   pip install -e .


This creates a new virtual environment with the necessary python dependencies and installs flake8-pyprojecttoml in editable mode. The flake8-pyprojecttoml code base uses pytest as its test runner, run the test suite by simply invoking::

   pytest
