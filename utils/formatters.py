def to_bullets(items: list | str) -> str:
    """Convert a list of strings to an HTML unordered list."""
    if isinstance(items, list):
        return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"
    return items
