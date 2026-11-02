#!/usr/bin/env python3
"""维护根目录的启停工具校验清单，并同步用户手册的下载与测试副本。"""

import argparse
import hashlib
import json
from pathlib import Path

from check_dev_policy import PolicyError, git, remote_url

ROOT = Path(__file__).resolve().parents[1]
FILES = ("friday-services.py", "start-friday.sh", "stop-friday.sh",
         "restart-friday.sh", "FRIDAY-SCRIPT-LICENSE.txt")


def planned_files(guide=None):
    content = {name: (ROOT / name).read_bytes() for name in FILES}
    sums = "".join(hashlib.sha256(content[name]).hexdigest() + "  " + name + "\n" for name in FILES).encode()
    planned = [(ROOT / "SHA256SUMS", sums, "source:SHA256SUMS")]
    if guide is not None:
        if (Path(git(guide, "rev-parse", "--show-toplevel")).resolve() != guide
                or remote_url(git(guide, "config", "--get", "remote.origin.url"))
                != "https://github.com/lijunfeng722/friday-user-guide"):
            raise ValueError("guide_repository_mismatch")
        for name, value in {**content, "SHA256SUMS": sums}.items():
            relative = "docs/assets/scripts/" + name
            planned.append((guide / relative, value, "guide:" + relative))
        relative = "scripts/test_services.py"
        planned.append((guide / relative, (ROOT / relative).read_bytes(), "guide:" + relative))
    for path, _, _ in planned:
        # 仅同步公开程序及测试，不沿链接覆盖部署电脑上的配置或其他文件。
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise ValueError("generated_path_is_symlink")
    return planned


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guide", type=Path, help="用户手册仓库根目录；省略时仅核对元仓库")
    parser.add_argument("--check", action="store_true", help="只检查，不改写文件")
    args = parser.parse_args()
    try:
        guide = args.guide.expanduser().resolve() if args.guide else None
        differences = []
        changed = 0
        for path, content, label in planned_files(guide):
            if path.is_file() and path.read_bytes() == content:
                continue
            differences.append(label)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                path.chmod(0o644)
                changed += 1
        report = {"ok": not differences if args.check else True,
                  "changed_files": changed, "differences": differences}
    except (OSError, ValueError, PolicyError):
        report = {"ok": False, "errors": ["service_distribution_check_failed"]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
