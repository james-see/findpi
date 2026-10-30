"""Smoke tests for findpi."""

import re

from findpi import __version__
from findpi.findpi import checkCores, getInput, getip, prep


def test_version_format() -> None:
    assert re.match(r"^\d+\.\d+\.\d+$", __version__)


def test_check_cores_returns_positive_int() -> None:
    assert isinstance(checkCores(), int)
    assert checkCores() > 0


def test_getip_returns_cidr_subnet() -> None:
    subnet = getip()
    assert subnet.endswith("/24")


def test_prep_defaults(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["findpi"])
    args = prep()
    assert args.cores is None


def test_get_input_single_host(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda prompt: "127.0.0.1/32")
    getInput("192.168.1.0/24", 1)
    output = capsys.readouterr().out
    assert "Checking for delicious pi" in output
