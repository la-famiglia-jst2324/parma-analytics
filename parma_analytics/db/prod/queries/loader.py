"""Helper functions for loading queries from sql files."""

from pathlib import Path

import sqlalchemy


def read_query_file(
    path: Path, /, replacements: dict[str, str] = {}
) -> sqlalchemy.TextClause:
    """Reads in sql query from a plain text file (e.g. .sql) with placeholders.

    Args:
        path: Path to template file
        replacements: dictionary of placeholders and their replacements

    Returns:
        The content of the file with filled placeholders
    """
    with open(path) as f:
        file_contents = f.read()
    for placeholder, replacement in replacements.items():
        file_contents = file_contents.replace(placeholder, replacement)
    return sqlalchemy.text(file_contents)
