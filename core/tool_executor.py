"""Tool executor: bridges the LLM tool calls and the PluginManager."""

import logging
from typing import Any

from core.plugin_manager import PluginManager

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Exposes the three core tools (add_plugin, run_plugin, unload_plugin) to the LLM."""

    def __init__(self, plugin_manager: PluginManager) -> None:
        """Initialise with a PluginManager instance."""
        self._pm = plugin_manager

    def add_plugin(self, name: str, code: str) -> dict[str, Any]:
        """Write *code* as plugin *name* and hot-reload it.

        Returns a dict with ``status`` on success or ``error`` on failure.
        """
        logger.info("Tool: add_plugin(%r)", name)
        return self._pm.add_plugin(name, code)

    def run_plugin(self, name: str, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute plugin *name* with *input_data*.

        Returns the plugin's result dict or an error dict.
        """
        logger.info("Tool: run_plugin(%r, %s)", name, list(input_data.keys()))
        return self._pm.call_plugin(name, input_data)

    def unload_plugin(self, name: str) -> dict[str, Any]:
        """Shut down and remove plugin *name* from the registry.

        Returns a dict with ``status`` on success or ``error`` on failure.
        """
        logger.info("Tool: unload_plugin(%r)", name)
        return self._pm.unload_plugin(name)
