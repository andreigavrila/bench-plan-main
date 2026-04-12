#!/usr/bin/env python3
"""Download the public evaluator bundle into the local benchmark checkout."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_OWNER = "bladnman"
DEFAULT_REPO = "planning_benchmark_evaluator"
DEFAULT_REF = "main"
DEFAULT_VERSION = "requirements_catalog_v1"


def build_url(owner: str, repo: str, ref: str, filename: str) -> str:
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{filename}"


def download_text(url: str) -> bytes:
    with urllib.request.urlopen(url) as response:
        return response.read()


def write_if_changed(path: Path, content: bytes) -> str:
    existed = path.exists()
    if existed and path.read_bytes() == content:
        return "unchanged"
    path.write_bytes(content)
    return "updated" if existed else "created"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument(
        "--dest",
        default="evaluator",
        help="Destination directory for downloaded evaluator files (default: evaluator)",
    )
    args = parser.parse_args()

    dest_dir = Path(args.dest).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)

    filenames = [f"{args.version}.md", f"{args.version}.json"]
    for filename in filenames:
        url = build_url(args.owner, args.repo, args.ref, filename)
        try:
            content = download_text(url)
        except urllib.error.HTTPError as exc:
            print(f"Failed to download {url}: HTTP {exc.code}", file=sys.stderr)
            return 1
        except urllib.error.URLError as exc:
            print(f"Failed to download {url}: {exc.reason}", file=sys.stderr)
            return 1

        destination = dest_dir / filename
        status = write_if_changed(destination, content)
        print(f"{status}: {destination}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
