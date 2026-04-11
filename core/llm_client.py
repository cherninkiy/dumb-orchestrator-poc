"""LLM client wrapping the Anthropic API with tool-use support."""

import logging
from typing import Any

import anthropic

logger = logging.getLogger(__name__)


class LLMClient:
    """Thin wrapper around ``anthropic.Anthropic`` with tool-use support."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
    ) -> None:
        """Initialise the client.

        Args:
            api_key: Anthropic API key.
            model: Model identifier to use for all requests.
        """
        self.model = model
        self._client = anthropic.Anthropic(api_key=api_key)

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        system: str = "",
    ) -> dict[str, Any]:
        """Send *messages* to the LLM and return a normalised response.

        Args:
            messages: Conversation history in Anthropic message format.
            tools: List of tool definitions (Anthropic tool-use schema).
            system: Optional system prompt string.

        Returns:
            A dict with either::

                {"type": "text", "content": <str>}

            or::

                {"type": "tool_calls", "tool_calls": [
                    {"id": <str>, "name": <str>, "input": <dict>}, ...
                ], "raw": <Message>}
        """
        try:
            kwargs: dict[str, Any] = {
                "model": self.model,
                "max_tokens": 4096,
                "messages": messages,
                "tools": tools,
            }
            if system:
                kwargs["system"] = system

            response = self._client.messages.create(**kwargs)
        except anthropic.APIError as exc:
            logger.error("Anthropic API error: %s", exc)
            raise

        stop_reason = response.stop_reason

        if stop_reason == "tool_use":
            tool_calls = [
                {
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                }
                for block in response.content
                if block.type == "tool_use"
            ]
            return {"type": "tool_calls", "tool_calls": tool_calls, "raw": response}

        # "end_turn" or any other stop reason → extract text
        text_parts = [block.text for block in response.content if hasattr(block, "text")]
        content = "\n".join(text_parts).strip()
        return {"type": "text", "content": content, "raw": response}
