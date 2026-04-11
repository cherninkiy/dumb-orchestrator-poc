"""Tests for ToolExecutor."""

from unittest.mock import MagicMock

import pytest

from core.tool_executor import ToolExecutor


@pytest.fixture()
def mock_pm() -> MagicMock:
    pm = MagicMock()
    return pm


@pytest.fixture()
def executor(mock_pm: MagicMock) -> ToolExecutor:
    return ToolExecutor(mock_pm)


def test_add_plugin_delegates_to_pm(executor: ToolExecutor, mock_pm: MagicMock) -> None:
    mock_pm.add_plugin.return_value = {"status": "ok", "plugin": "myplugin"}
    result = executor.add_plugin("myplugin", "def run(d): return d")
    mock_pm.add_plugin.assert_called_once_with("myplugin", "def run(d): return d")
    assert result == {"status": "ok", "plugin": "myplugin"}


def test_run_plugin_delegates_to_pm(executor: ToolExecutor, mock_pm: MagicMock) -> None:
    mock_pm.call_plugin.return_value = {"result": 42}
    result = executor.run_plugin("calc", {"x": 1})
    mock_pm.call_plugin.assert_called_once_with("calc", {"x": 1})
    assert result == {"result": 42}


def test_unload_plugin_delegates_to_pm(executor: ToolExecutor, mock_pm: MagicMock) -> None:
    mock_pm.unload_plugin.return_value = {"status": "ok", "plugin": "old"}
    result = executor.unload_plugin("old")
    mock_pm.unload_plugin.assert_called_once_with("old")
    assert result == {"status": "ok", "plugin": "old"}


def test_add_plugin_propagates_error(executor: ToolExecutor, mock_pm: MagicMock) -> None:
    mock_pm.add_plugin.return_value = {"error": "syntax error"}
    result = executor.add_plugin("bad", "not python")
    assert "error" in result


def test_run_plugin_propagates_error(executor: ToolExecutor, mock_pm: MagicMock) -> None:
    mock_pm.call_plugin.return_value = {"error": "plugin not loaded"}
    result = executor.run_plugin("missing", {})
    assert "error" in result
