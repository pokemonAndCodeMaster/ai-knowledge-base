#!/usr/bin/env python3
"""验证 NotebookLM Markdown 导出目录的数量、字节数与 SHA-256。"""

import argparse
import hashlib
import re
from pathlib import Path


ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*\[([^]]+)\]"
    r".*?\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|$"
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("export_dir", type=Path)
    parser.add_argument("--expected-count", type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    manifest_path = args.export_dir / "_MANIFEST.md"
    if not manifest_path.is_file():
        raise SystemExit(f"FAIL: 缺少 {manifest_path}")

    rows = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        match = ROW_RE.match(line)
        if match:
            index, source_id, filename, size, chars, lines, digest = match.groups()
            rows[int(index)] = {
                "source_id": source_id,
                "filename": filename,
                "bytes": int(size),
                "chars": int(chars),
                "lines": int(lines),
                "sha256": digest,
            }

    files = sorted(args.export_dir.glob("[0-9][0-9]_*.md"))
    expected = args.expected_count if args.expected_count is not None else len(rows)
    errors = []
    if len(rows) != expected:
        errors.append(f"Manifest={len(rows)}，预期={expected}")
    if len(files) != expected:
        errors.append(f"文件={len(files)}，预期={expected}")
    if len({row['source_id'] for row in rows.values()}) != len(rows):
        errors.append("source_id 不唯一")

    hashes = []
    for index, file in enumerate(files, 1):
        row = rows.get(index)
        if not row:
            errors.append(f"{file.name}: Manifest 缺少序号 {index}")
            continue
        data = file.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"{file.name}: 非 UTF-8：{error}")
            continue
        digest = hashlib.sha256(data).hexdigest()
        hashes.append(digest)
        js_chars = len(text.encode("utf-16-le")) // 2
        line_count = len(text.splitlines()) + (1 if text.endswith("\n") else 0)
        actual = (file.name, len(data), js_chars, line_count, digest)
        expected_values = (
            row["filename"], row["bytes"], row["chars"], row["lines"], row["sha256"]
        )
        if actual != expected_values:
            errors.append(f"{file.name}: Manifest 不一致")

    print(
        {
            "expected": expected,
            "manifest_rows": len(rows),
            "files": len(files),
            "unique_hashes": len(set(hashes)),
            "duplicate_files": len(hashes) - len(set(hashes)),
            "errors": errors,
        }
    )
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
