"""Flake8 extension to add pyproject.toml support."""
from __future__ import annotations

import configparser
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

import flake8

if sys.version_info < (3, 11):  # pragma: no cover
    import tomli as tomllib
else:  # pragma: no cover
    import tomllib

if TYPE_CHECKING:
    from typing import Generator, TextIO

    from flake8.options.manager import OptionManager

FLAKE8_MAJOR_VERSION = int(flake8.__version__.split(".")[0])


class Dummy:  # pylint: disable=too-few-public-methods
    """Dummy class used as reporter entry point."""


def _update_flake8_section(parser: configparser.RawConfigParser, data: dict):
    if not parser.has_section("flake8"):
        parser.add_section("flake8")
    for key, value in data.items():
        value = str(value) if isinstance(value, bool) else value
        parser.set("flake8", key, value)


if FLAKE8_MAJOR_VERSION >= 5:

    from flake8.options import aggregator

    _aggregate_options = aggregator.aggregate_options

    def aggregate_options(
        manager: OptionManager, cfg: configparser.ConfigParser, cfg_dir: str, argv: list
    ):
        pyproj = os.path.join(cfg_dir, "pyproject.toml")
        with open(pyproj, "rb") as f:
            if data := tomllib.load(f).get("tool", {}).get("flake8"):
                _update_flake8_section(cfg, data)
        return _aggregate_options(manager, cfg, cfg_dir, argv)

    aggregator.aggregate_options = aggregate_options

else:
    from flake8.options import config  # type: ignore

    class ConfigParser(configparser.RawConfigParser):
        """Add toml support to flake8's config parser."""

        def _read(self, fp: TextIO, fpname: str) -> None:
            if Path(fpname).name == "pyproject.toml":
                if cfg := tomllib.load(fp.buffer).get("tool", {}).get("flake8"):
                    _update_flake8_section(self, cfg)
                return
            super()._read(fp, fpname)  # type: ignore

    _generate_possible_local_files = (
        config.ConfigFileFinder.generate_possible_local_files
    )

    def generate_possible_local_files(
        cff: config.ConfigFileFinder,
    ) -> Generator[str, None, None]:
        """Find and generate all local config files."""
        cff.project_filenames = cff.project_filenames + ("pyproject.toml",)
        yield from _generate_possible_local_files(cff)

    patched_configparser = ModuleType("configparser")
    patched_configparser.ParsingError = configparser.ParsingError  # type: ignore
    patched_configparser.RawConfigParser = ConfigParser  # type: ignore
    config.configparser = patched_configparser
    config.ConfigFileFinder.generate_possible_local_files = (
        generate_possible_local_files
    )
