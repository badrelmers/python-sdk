import asyncio
import contextlib
import os
from pathlib import Path

import pytest

from acp import PROTOCOL_VERSION, connect_to_agent, text_block
from acp.schema import ClientCapabilities, Implementation
from examples.client import ExampleClient

ENV_VAR = "ACP_QWEN_CODE_CLI_BIN"
PROMPT_TIMEOUT = 60.0


class RecordingClient(ExampleClient):
    def __init__(self) -> None:
        super().__init__()
        self._update_event = asyncio.Event()
        self.received_chunks: list[str] = []

    async def session_update(self, session_id, update, **kwargs):  # type: ignore[override]
        from acp.schema import AgentMessageChunk, TextContentBlock

        if not isinstance(update, AgentMessageChunk):
            return
        content = update.content
        if isinstance(content, TextContentBlock):
            self.received_chunks.append(content.text)
            self._update_event.set()

    async def wait_for_chunk(self, timeout: float) -> None:
        await asyncio.wait_for(self._update_event.wait(), timeout=timeout)


@pytest.mark.asyncio
async def test_qwen_cli_prompt() -> None:
    cli_path = os.getenv(ENV_VAR)
    if not cli_path:
        pytest.skip(f"Set {ENV_VAR} to the Qwen Code CLI executable to run this test")

    resolved = Path(cli_path).expanduser()
    if not resolved.exists():
        pytest.skip(f"Qwen Code CLI binary not found at {resolved}")

    proc = await asyncio.create_subprocess_exec(
        str(resolved),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )

    assert proc.stdin is not None and proc.stdout is not None, "Agent did not expose stdio pipes"

    client = RecordingClient()
    conn = connect_to_agent(client, proc.stdin, proc.stdout, use_unstable_protocol=True)

    await conn.initialize(
        protocol_version=PROTOCOL_VERSION,
        client_capabilities=ClientCapabilities(),
        client_info=Implementation(name="qwen-e2e-test", title="Qwen CLI Test", version="0.1.0"),
    )

    session = await conn.new_session(cwd=os.getcwd(), mcp_servers=[])

    await conn.prompt(
        session_id=session.session_id,
        prompt=[text_block("Summarize what the Qwen Code CLI agent can do.")],
    )

    await client.wait_for_chunk(PROMPT_TIMEOUT)
    assert client.received_chunks, "Agent did not return any text content"

    proc.terminate()
    with contextlib.suppress(ProcessLookupError):
        await proc.wait()
