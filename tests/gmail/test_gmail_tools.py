"""Tests for the Gmail _resolve_reply_context helper.

The helper looks up an original message by its Gmail message ID and returns
(thread_id, in_reply_to, references) so that send_gmail_message and
draft_gmail_message can take a single `reply_to_message_id` arg instead of
making the caller hand-build the threading triple.

We test the helper directly. The param-wiring on send_gmail_message and
draft_gmail_message is exercised by the end-to-end smoke step in the plan,
not unit tests, because the production functions are wrapped by
require_google_service / handle_http_errors / server.tool() which would
require multi-layer decorator bypass to invoke from a test.
"""

import sys
import os
import pytest
from unittest.mock import Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from gmail.gmail_tools import _resolve_reply_context


def _make_service(message_response):
    """Build a mock Gmail service whose messages().get(...).execute returns message_response."""
    service = Mock()
    service.users.return_value.messages.return_value.get.return_value.execute = Mock(
        return_value=message_response
    )
    return service


@pytest.mark.asyncio
async def test_resolve_reply_context_with_references_header():
    """References header present → returned references chain appends Message-ID."""
    service = _make_service(
        {
            "threadId": "T1",
            "payload": {
                "headers": [
                    {"name": "Message-ID", "value": "<orig@example.com>"},
                    {"name": "References", "value": "<a@example.com> <b@example.com>"},
                ]
            },
        }
    )

    thread_id, in_reply_to, references = await _resolve_reply_context(service, "msg-123")

    assert thread_id == "T1"
    assert in_reply_to == "<orig@example.com>"
    assert references == "<a@example.com> <b@example.com> <orig@example.com>"


@pytest.mark.asyncio
async def test_resolve_reply_context_without_references_header():
    """No References header → references == Message-ID alone."""
    service = _make_service(
        {
            "threadId": "T1",
            "payload": {
                "headers": [
                    {"name": "Message-ID", "value": "<orig@example.com>"},
                ]
            },
        }
    )

    thread_id, in_reply_to, references = await _resolve_reply_context(service, "msg-123")

    assert thread_id == "T1"
    assert in_reply_to == "<orig@example.com>"
    assert references == "<orig@example.com>"


@pytest.mark.asyncio
async def test_resolve_reply_context_missing_message_id_raises():
    """Original message lacks a Message-ID header → ValueError, not silent None."""
    service = _make_service(
        {
            "threadId": "T1",
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "anything"},
                ]
            },
        }
    )

    with pytest.raises(ValueError, match="Message-ID"):
        await _resolve_reply_context(service, "msg-123")


@pytest.mark.asyncio
async def test_resolve_reply_context_propagates_lookup_errors():
    """If the Gmail API call raises (e.g. 404), the error propagates — no silent fallback."""
    service = Mock()
    service.users.return_value.messages.return_value.get.return_value.execute = Mock(
        side_effect=RuntimeError("404 not found")
    )

    with pytest.raises(RuntimeError, match="404"):
        await _resolve_reply_context(service, "missing-msg-id")


@pytest.mark.asyncio
async def test_resolve_reply_context_uses_metadata_format():
    """Sanity: the helper requests metadata format with Message-ID + References headers."""
    service = _make_service(
        {
            "threadId": "T1",
            "payload": {
                "headers": [{"name": "Message-ID", "value": "<orig@example.com>"}]
            },
        }
    )

    await _resolve_reply_context(service, "msg-123")

    call_kwargs = service.users.return_value.messages.return_value.get.call_args.kwargs
    assert call_kwargs["userId"] == "me"
    assert call_kwargs["id"] == "msg-123"
    assert call_kwargs["format"] == "metadata"
    assert "Message-ID" in call_kwargs["metadataHeaders"]
    assert "References" in call_kwargs["metadataHeaders"]
