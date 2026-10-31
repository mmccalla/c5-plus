"""Run the viewer's real JavaScript (minus D3 paint) under Node."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
HARNESS = ROOT / "viewer_runtime.mjs"


def viewer_op(op: dict[str, Any]) -> dict[str, Any]:
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("node is required to execute index.html")
    proc = subprocess.run(
        [node, str(HARNESS)],
        input=json.dumps(op),
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(proc.stderr or proc.stdout or "viewer harness failed")
    line = proc.stdout.strip().splitlines()[-1]
    return json.loads(line)
