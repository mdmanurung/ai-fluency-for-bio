"""Convert a module README.md into a paired runnable notebook.ipynb.

Splits the README on fenced ```python blocks: prose becomes markdown cells,
python blocks become code cells. ```bash blocks and unfenced (prompt) blocks
stay in markdown cells. The first H1 heading is preserved at the top.

Usage:
    python tools/readme_to_ipynb.py path/to/README.md path/to/notebook.ipynb

The script is idempotent — re-run after editing a README to regenerate the
notebook. Manual edits to the notebook will be lost; treat the README as the
source of truth.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PYTHON_BLOCK = re.compile(r"```python\n(.*?)\n```", re.DOTALL)


def split_cells(text: str) -> list[tuple[str, str]]:
    """Return [(kind, content), ...] where kind is 'markdown' or 'code'."""
    cells: list[tuple[str, str]] = []
    last = 0
    for m in PYTHON_BLOCK.finditer(text):
        before = text[last : m.start()].strip("\n")
        if before:
            cells.append(("markdown", before))
        cells.append(("code", m.group(1)))
        last = m.end()
    tail = text[last:].strip("\n")
    if tail:
        cells.append(("markdown", tail))
    return cells


def to_notebook(cells: list[tuple[str, str]]) -> dict:
    nb_cells: list[dict] = []
    for kind, content in cells:
        if kind == "markdown":
            nb_cells.append(
                {"cell_type": "markdown", "metadata": {}, "source": content}
            )
        else:
            nb_cells.append(
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": content,
                }
            )
    return {
        "cells": nb_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1]).read_text()
    dst = Path(sys.argv[2])
    nb = to_notebook(split_cells(src))
    dst.write_text(json.dumps(nb, indent=1) + "\n")
    print(f"wrote {dst} ({len(nb['cells'])} cells)")


if __name__ == "__main__":
    main()
