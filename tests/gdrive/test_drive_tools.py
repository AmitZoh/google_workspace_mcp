"""
Unit tests for Google Drive MCP tools.

Tests create_drive_folder with mocked API responses.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


def _make_http_error(status: int, reason: str = "notFound") -> HttpError:
    """Build an HttpError mimicking what google-api-python-client raises."""
    resp = Mock()
    resp.status = status
    resp.reason = reason
    return HttpError(resp=resp, content=b'{"error": {"message": "test"}}')


@pytest.mark.asyncio
async def test_create_drive_folder():
    """Test create_drive_folder returns success message with folder id, name, and link."""
    from gdrive.drive_tools import _create_drive_folder_impl

    mock_service = Mock()
    mock_response = {
        "id": "folder123",
        "name": "My Folder",
        "webViewLink": "https://drive.google.com/drive/folders/folder123",
    }
    mock_request = Mock()
    mock_request.execute.return_value = mock_response
    mock_service.files.return_value.create.return_value = mock_request

    with patch(
        "gdrive.drive_tools.resolve_folder_id",
        new_callable=AsyncMock,
        return_value="root",
    ):
        result = await _create_drive_folder_impl(
            service=mock_service,
            user_google_email="user@example.com",
            folder_name="My Folder",
            parent_folder_id="root",
        )

    assert "Successfully created folder" in result
    assert "My Folder" in result
    assert "folder123" in result
    assert "user@example.com" in result
    assert "https://drive.google.com/drive/folders/folder123" in result


@pytest.mark.asyncio
async def test_resolve_folder_id_permissive_passes_through_on_success():
    """When resolve_folder_id succeeds, return its result unchanged."""
    from gdrive.drive_tools import _resolve_folder_id_permissive

    with patch(
        "gdrive.drive_tools.resolve_folder_id",
        new_callable=AsyncMock,
        return_value="resolved_target_id",
    ):
        result = await _resolve_folder_id_permissive(Mock(), "shortcut_id")

    assert result == "resolved_target_id"


@pytest.mark.asyncio
async def test_resolve_folder_id_permissive_falls_back_on_404():
    """Under drive.file scope, files.get 404s on user-created folders.
    The helper must fall through with the raw folder_id."""
    from gdrive.drive_tools import _resolve_folder_id_permissive

    with patch(
        "gdrive.drive_tools.resolve_folder_id",
        new_callable=AsyncMock,
        side_effect=_make_http_error(404),
    ):
        result = await _resolve_folder_id_permissive(Mock(), "user_folder_id")

    assert result == "user_folder_id"


@pytest.mark.asyncio
async def test_resolve_folder_id_permissive_falls_back_on_403():
    """403 (PermissionDenied) on the pre-check is also a drive.file symptom."""
    from gdrive.drive_tools import _resolve_folder_id_permissive

    with patch(
        "gdrive.drive_tools.resolve_folder_id",
        new_callable=AsyncMock,
        side_effect=_make_http_error(403, "forbidden"),
    ):
        result = await _resolve_folder_id_permissive(Mock(), "user_folder_id")

    assert result == "user_folder_id"


@pytest.mark.asyncio
async def test_resolve_folder_id_permissive_propagates_other_http_errors():
    """500/400/etc. are not scope-related; the original error must propagate."""
    from gdrive.drive_tools import _resolve_folder_id_permissive

    err = _make_http_error(500, "serverError")
    with patch(
        "gdrive.drive_tools.resolve_folder_id",
        new_callable=AsyncMock,
        side_effect=err,
    ):
        with pytest.raises(HttpError) as exc_info:
            await _resolve_folder_id_permissive(Mock(), "user_folder_id")

    assert exc_info.value.resp.status == 500


@pytest.mark.asyncio
async def test_resolve_folder_id_permissive_does_not_fall_back_for_root():
    """folder_id='root' failing is a real config problem, not a scope issue —
    the user can always GET their own root. Propagate."""
    from gdrive.drive_tools import _resolve_folder_id_permissive

    with patch(
        "gdrive.drive_tools.resolve_folder_id",
        new_callable=AsyncMock,
        side_effect=_make_http_error(404),
    ):
        with pytest.raises(HttpError):
            await _resolve_folder_id_permissive(Mock(), "root")
