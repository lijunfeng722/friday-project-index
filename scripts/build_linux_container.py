"""兼容旧维护入口，构建实现与 Dockerfile 统一由 Friday 仓库维护。"""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('--friday',type=Path,default=Path(__file__).resolve().parents[2]/'Friday')
    args,remaining=parser.parse_known_args()
    source=args.friday.resolve()
    return subprocess.run([sys.executable,str(source/'scripts/build_linux_container.py'),
                           '--friday',str(source),*remaining]).returncode


if __name__=='__main__':raise SystemExit(main())
