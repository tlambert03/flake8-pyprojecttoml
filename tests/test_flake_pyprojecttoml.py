"""Test suite."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest
from flake8.main.application import Application  # type: ignore

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

TESTCASES = [
    (
        [],
        [],
        [
            '1:1: D100 Missing docstring in public module',
        ],
    ),
    (
        ['[tool.flake8]', 'ignore = ["D100"]'],
        [],
        [],
    ),
    (
        ['[tool.flake8]'],
        ['#' * 99, '"""Docstring."""', ''],
        ['1:80: E501 line too long (99 > 79 characters)'],
    ),
    (
        ['[tool.flake8]', 'max_line_length = 100'],
        ['#' * 99, '"""Docstring."""', ''],
        [],
    ),
]


@pytest.mark.parametrize(('config', 'code', 'expected'), TESTCASES)
def test_config_is_being_used(
    config: list[str],
    code: list[str],
    expected: str,
    capsys: Any,  # noqa: ANN401
    tmp_path: Path,
) -> None:
    """Test config is being used."""
    configpath = tmp_path / 'pyproject.toml'
    codepath = tmp_path / 'code.py'

    configpath.write_text('\n'.join(config))
    codepath.write_text('\n'.join(code))

    with patch('os.getcwd', return_value=str(tmp_path)):
        app = Application()
        app.run([str(codepath)])
    captured = capsys.readouterr()
    for have, expect in zip(captured.out.split('\n'), expected):
        assert have == f'{codepath}:{expect}'
