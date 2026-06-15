"""
Google Workspace OAuth Scopes

This module centralizes OAuth scope definitions for Google Workspace integration.
Separated from service_decorator.py to avoid circular imports.
"""

import logging

logger = logging.getLogger(__name__)

# Global variable to store enabled tools (set by main.py)
_ENABLED_TOOLS = None

# Individual OAuth Scope Constants
USERINFO_EMAIL_SCOPE = "https://www.googleapis.com/auth/userinfo.email"
USERINFO_PROFILE_SCOPE = "https://www.googleapis.com/auth/userinfo.profile"
OPENID_SCOPE = "openid"
CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar"
CALENDAR_READONLY_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"
CALENDAR_EVENTS_SCOPE = "https://www.googleapis.com/auth/calendar.events"

# Google Drive scopes
DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"
DRIVE_READONLY_SCOPE = "https://www.googleapis.com/auth/drive.readonly"
DRIVE_FILE_SCOPE = "https://www.googleapis.com/auth/drive.file"

# Google Docs scopes
DOCS_READONLY_SCOPE = "https://www.googleapis.com/auth/documents.readonly"
DOCS_WRITE_SCOPE = "https://www.googleapis.com/auth/documents"

# Gmail API scopes
GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
GMAIL_COMPOSE_SCOPE = "https://www.googleapis.com/auth/gmail.compose"
GMAIL_MODIFY_SCOPE = "https://www.googleapis.com/auth/gmail.modify"
GMAIL_LABELS_SCOPE = "https://www.googleapis.com/auth/gmail.labels"
GMAIL_SETTINGS_BASIC_SCOPE = "https://www.googleapis.com/auth/gmail.settings.basic"

# Google Chat API scopes
CHAT_READONLY_SCOPE = "https://www.googleapis.com/auth/chat.messages.readonly"
CHAT_WRITE_SCOPE = "https://www.googleapis.com/auth/chat.messages"
CHAT_SPACES_SCOPE = "https://www.googleapis.com/auth/chat.spaces"
CHAT_SPACES_READONLY_SCOPE = "https://www.googleapis.com/auth/chat.spaces.readonly"

# Google Sheets API scopes
SHEETS_READONLY_SCOPE = "https://www.googleapis.com/auth/spreadsheets.readonly"
SHEETS_WRITE_SCOPE = "https://www.googleapis.com/auth/spreadsheets"

# Google Forms API scopes
FORMS_BODY_SCOPE = "https://www.googleapis.com/auth/forms.body"
FORMS_BODY_READONLY_SCOPE = "https://www.googleapis.com/auth/forms.body.readonly"
FORMS_RESPONSES_READONLY_SCOPE = (
    "https://www.googleapis.com/auth/forms.responses.readonly"
)

# Google Slides API scopes
SLIDES_SCOPE = "https://www.googleapis.com/auth/presentations"
SLIDES_READONLY_SCOPE = "https://www.googleapis.com/auth/presentations.readonly"

# Google Tasks API scopes
TASKS_SCOPE = "https://www.googleapis.com/auth/tasks"
TASKS_READONLY_SCOPE = "https://www.googleapis.com/auth/tasks.readonly"

# Google Contacts (People API) scopes
CONTACTS_SCOPE = "https://www.googleapis.com/auth/contacts"
CONTACTS_READONLY_SCOPE = "https://www.googleapis.com/auth/contacts.readonly"
DIRECTORY_READONLY_SCOPE = "https://www.googleapis.com/auth/directory.readonly"

# Google Custom Search API scope
CUSTOM_SEARCH_SCOPE = "https://www.googleapis.com/auth/cse"

# Google Apps Script API scopes
SCRIPT_PROJECTS_SCOPE = "https://www.googleapis.com/auth/script.projects"
SCRIPT_PROJECTS_READONLY_SCOPE = (
    "https://www.googleapis.com/auth/script.projects.readonly"
)
SCRIPT_DEPLOYMENTS_SCOPE = "https://www.googleapis.com/auth/script.deployments"
SCRIPT_DEPLOYMENTS_READONLY_SCOPE = (
    "https://www.googleapis.com/auth/script.deployments.readonly"
)
SCRIPT_PROCESSES_READONLY_SCOPE = "https://www.googleapis.com/auth/script.processes"
SCRIPT_METRICS_SCOPE = "https://www.googleapis.com/auth/script.metrics"

# Google scope hierarchy: broader scopes that implicitly cover narrower ones.
# See https://developers.google.com/gmail/api/auth/scopes,
# https://developers.google.com/drive/api/guides/api-specific-auth, etc.
SCOPE_HIERARCHY = {
    GMAIL_MODIFY_SCOPE: {
        GMAIL_READONLY_SCOPE,
        GMAIL_SEND_SCOPE,
        GMAIL_COMPOSE_SCOPE,
        GMAIL_LABELS_SCOPE,
    },
    DRIVE_SCOPE: {DRIVE_READONLY_SCOPE, DRIVE_FILE_SCOPE},
    CALENDAR_SCOPE: {CALENDAR_READONLY_SCOPE, CALENDAR_EVENTS_SCOPE},
    DOCS_WRITE_SCOPE: {DOCS_READONLY_SCOPE},
    SHEETS_WRITE_SCOPE: {SHEETS_READONLY_SCOPE},
    SLIDES_SCOPE: {SLIDES_READONLY_SCOPE},
    TASKS_SCOPE: {TASKS_READONLY_SCOPE},
    CONTACTS_SCOPE: {CONTACTS_READONLY_SCOPE},
    CHAT_WRITE_SCOPE: {CHAT_READONLY_SCOPE},
    CHAT_SPACES_SCOPE: {CHAT_SPACES_READONLY_SCOPE},
    FORMS_BODY_SCOPE: {FORMS_BODY_READONLY_SCOPE},
    SCRIPT_PROJECTS_SCOPE: {SCRIPT_PROJECTS_READONLY_SCOPE},
    SCRIPT_DEPLOYMENTS_SCOPE: {SCRIPT_DEPLOYMENTS_READONLY_SCOPE},
}


def has_required_scopes(available_scopes, required_scopes):
    """
    Check if available scopes satisfy all required scopes, accounting for
    Google's scope hierarchy (e.g., gmail.modify covers gmail.readonly).

    Args:
        available_scopes: Scopes the credentials have (set, list, or frozenset).
        required_scopes: Scopes that are required (set, list, or frozenset).

    Returns:
        True if all required scopes are satisfied.
    """
    available = set(available_scopes or [])
    required = set(required_scopes or [])
    # Expand available scopes with implied narrower scopes
    expanded = set(available)
    for broad_scope, covered in SCOPE_HIERARCHY.items():
        if broad_scope in available:
            expanded.update(covered)
    return all(scope in expanded for scope in required)


# Base OAuth scopes required for user identification
BASE_SCOPES = [USERINFO_EMAIL_SCOPE, USERINFO_PROFILE_SCOPE, OPENID_SCOPE]

# Service-specific scope groups
DOCS_SCOPES = [
    DOCS_READONLY_SCOPE,
    DOCS_WRITE_SCOPE,
    DRIVE_READONLY_SCOPE,
    DRIVE_FILE_SCOPE,
]

CALENDAR_SCOPES = [CALENDAR_SCOPE, CALENDAR_READONLY_SCOPE, CALENDAR_EVENTS_SCOPE]

DRIVE_SCOPES = [DRIVE_SCOPE, DRIVE_READONLY_SCOPE, DRIVE_FILE_SCOPE]

GMAIL_SCOPES = [
    GMAIL_READONLY_SCOPE,
    GMAIL_SEND_SCOPE,
    GMAIL_COMPOSE_SCOPE,
    GMAIL_MODIFY_SCOPE,
    GMAIL_LABELS_SCOPE,
    GMAIL_SETTINGS_BASIC_SCOPE,
]

CHAT_SCOPES = [
    CHAT_READONLY_SCOPE,
    CHAT_WRITE_SCOPE,
    CHAT_SPACES_SCOPE,
    CHAT_SPACES_READONLY_SCOPE,
]

SHEETS_SCOPES = [SHEETS_READONLY_SCOPE, SHEETS_WRITE_SCOPE, DRIVE_READONLY_SCOPE]

FORMS_SCOPES = [
    FORMS_BODY_SCOPE,
    FORMS_BODY_READONLY_SCOPE,
    FORMS_RESPONSES_READONLY_SCOPE,
]

SLIDES_SCOPES = [SLIDES_SCOPE, SLIDES_READONLY_SCOPE]

TASKS_SCOPES = [TASKS_SCOPE, TASKS_READONLY_SCOPE]

CONTACTS_SCOPES = [CONTACTS_SCOPE, CONTACTS_READONLY_SCOPE, DIRECTORY_READONLY_SCOPE]

CUSTOM_SEARCH_SCOPES = [CUSTOM_SEARCH_SCOPE]

SCRIPT_SCOPES = [
    SCRIPT_PROJECTS_SCOPE,
    SCRIPT_PROJECTS_READONLY_SCOPE,
    SCRIPT_DEPLOYMENTS_SCOPE,
    SCRIPT_DEPLOYMENTS_READONLY_SCOPE,
    SCRIPT_PROCESSES_READONLY_SCOPE,  # Required for list_script_processes
    SCRIPT_METRICS_SCOPE,  # Required for get_script_metrics
    DRIVE_FILE_SCOPE,  # Required for list/delete script projects (uses Drive API)
]

# Tool-to-scopes mapping
TOOL_SCOPES_MAP = {
    "gmail": GMAIL_SCOPES,
    "drive": DRIVE_SCOPES,
    "calendar": CALENDAR_SCOPES,
    "docs": DOCS_SCOPES,
    "sheets": SHEETS_SCOPES,
    "chat": CHAT_SCOPES,
    "forms": FORMS_SCOPES,
    "slides": SLIDES_SCOPES,
    "tasks": TASKS_SCOPES,
    "contacts": CONTACTS_SCOPES,
    "search": CUSTOM_SEARCH_SCOPES,
    "appscript": SCRIPT_SCOPES,
}

# Tool-to-read-only-scopes mapping
TOOL_READONLY_SCOPES_MAP = {
    "gmail": [GMAIL_READONLY_SCOPE],
    "drive": [DRIVE_READONLY_SCOPE],
    "calendar": [CALENDAR_READONLY_SCOPE],
    "docs": [DOCS_READONLY_SCOPE, DRIVE_READONLY_SCOPE],
    "sheets": [SHEETS_READONLY_SCOPE, DRIVE_READONLY_SCOPE],
    "chat": [CHAT_READONLY_SCOPE, CHAT_SPACES_READONLY_SCOPE],
    "forms": [FORMS_BODY_READONLY_SCOPE, FORMS_RESPONSES_READONLY_SCOPE],
    "slides": [SLIDES_READONLY_SCOPE],
    "tasks": [TASKS_READONLY_SCOPE],
    "contacts": [CONTACTS_READONLY_SCOPE, DIRECTORY_READONLY_SCOPE],
    "search": CUSTOM_SEARCH_SCOPES,
    "appscript": [
        SCRIPT_PROJECTS_READONLY_SCOPE,
        SCRIPT_DEPLOYMENTS_READONLY_SCOPE,
        SCRIPT_PROCESSES_READONLY_SCOPE,
        SCRIPT_METRICS_SCOPE,
        DRIVE_READONLY_SCOPE,
    ],
}


def set_enabled_tools(enabled_tools):
    """
    Set the globally enabled tools list.

    Args:
        enabled_tools: List of enabled tool names.
    """
    global _ENABLED_TOOLS
    _ENABLED_TOOLS = enabled_tools
    logger.info(f"Enabled tools set for scope management: {enabled_tools}")


# Set of tool names that should be treated as read-only (set by main.py).
# Empty set = no read-only tools. Non-empty = at least one tool downgraded to its
# read-only scope set. Single source of truth for both global --read-only and
# per-tool --read-only <list> CLI behavior.
_READONLY_TOOLS: set[str] = set()


def set_readonly_tools(tool_names):
    """
    Mark the given tools as read-only. Composes with prior calls (union).

    Args:
        tool_names: Iterable of tool-group names (e.g. ["drive", "calendar"]).
            Names not in TOOL_SCOPES_MAP are kept in the set but have no effect
            on scope resolution; validation is the CLI layer's responsibility.
    """
    global _READONLY_TOOLS
    _READONLY_TOOLS.update(tool_names)
    logger.info(f"Read-only tools set to: {sorted(_READONLY_TOOLS)}")


def set_read_only(enabled: bool):
    """
    Set the global read-only mode (backward-compatible API).

    True puts every TOOL_SCOPES_MAP key in the read-only set ("everything readonly").
    False clears the set.

    Args:
        enabled: Boolean indicating if read-only mode should be enabled.
    """
    global _READONLY_TOOLS
    _READONLY_TOOLS = set(TOOL_SCOPES_MAP.keys()) if enabled else set()
    logger.info(f"Read-only mode set to: {enabled}")


def is_read_only_mode() -> bool:
    """True iff at least one tool is in read-only mode."""
    return bool(_READONLY_TOOLS)


def is_tool_read_only(tool: str) -> bool:
    """True iff the given tool-group is marked read-only."""
    return tool in _READONLY_TOOLS


def get_readonly_tools() -> set[str]:
    """Return a copy of the read-only tool set."""
    return set(_READONLY_TOOLS)


def get_allowed_scopes_for_filter(enabled_tools=None) -> list[str]:
    """
    Return the union of scopes that should be considered "allowed" when filtering
    tools in read-only mode. For each enabled tool, includes its read-only scope
    set if it's in _READONLY_TOOLS, otherwise its full scope set. Plus BASE_SCOPES.

    Used by core/tool_registry.py to decide which write tools to disable.

    Args:
        enabled_tools: List of tool-group names (gmail, drive, etc.). If None,
            falls back to the globally-set enabled-tools list (matches
            get_current_scopes() behavior), and finally to all tool groups.
    """
    if enabled_tools is None:
        enabled_tools = (
            _ENABLED_TOOLS if _ENABLED_TOOLS is not None else TOOL_SCOPES_MAP.keys()
        )

    allowed = set(BASE_SCOPES)
    for tool in enabled_tools:
        if tool in _READONLY_TOOLS:
            allowed.update(TOOL_READONLY_SCOPES_MAP.get(tool, []))
        else:
            allowed.update(TOOL_SCOPES_MAP.get(tool, []))
    return list(allowed)


def get_current_scopes():
    """
    Returns scopes for currently enabled tools.
    Uses globally set enabled tools or all tools if not set.

    .. deprecated::
        This function is a thin wrapper around get_scopes_for_tools() and exists
        for backwards compatibility. Prefer using get_scopes_for_tools() directly
        for new code, which allows explicit control over the tool list parameter.

    Returns:
        List of unique scopes for the enabled tools plus base scopes.
    """
    return get_scopes_for_tools(_ENABLED_TOOLS)


def get_scopes_for_tools(enabled_tools=None):
    """
    Returns scopes for enabled tools only.

    Args:
        enabled_tools: List of enabled tool names. If None, returns all scopes.

    Returns:
        List of unique scopes for the enabled tools plus base scopes.
    """
    if enabled_tools is None:
        # Default behavior - return all scopes
        enabled_tools = TOOL_SCOPES_MAP.keys()

    # Start with base scopes (always required)
    scopes = BASE_SCOPES.copy()

    # Per-tool scope-map selection: each enabled tool picks the read-only map iff
    # it's in _READONLY_TOOLS, else the full map.
    enabled_list = list(enabled_tools)
    readonly_for_enabled = [t for t in enabled_list if t in _READONLY_TOOLS]
    if not readonly_for_enabled:
        mode_str = "full"
    elif len(readonly_for_enabled) == len(enabled_list):
        mode_str = "read-only"
    else:
        mode_str = "mixed"

    for tool in enabled_list:
        if tool in _READONLY_TOOLS:
            scopes.extend(TOOL_READONLY_SCOPES_MAP.get(tool, []))
        elif tool in TOOL_SCOPES_MAP:
            scopes.extend(TOOL_SCOPES_MAP[tool])

    logger.debug(
        f"Generated {mode_str} scopes for tools {enabled_list}: {len(set(scopes))} unique scopes"
    )
    # Return unique scopes
    return list(set(scopes))


# Combined scopes for all supported Google Workspace operations (backwards compatibility)
SCOPES = get_scopes_for_tools()
