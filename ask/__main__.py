"""Start the local ask API: python -m ask."""

from __future__ import annotations

import uvicorn


def main() -> None:
    uvicorn.run("ask.server:app", host="127.0.0.1", port=8765)


if __name__ == "__main__":
    main()
