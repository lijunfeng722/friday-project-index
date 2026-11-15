"""调用 Friday 的独立容器验收，不再提供重启当前家庭容器的测试选项。"""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('--friday',type=Path,default=Path(__file__).resolve().parents[2]/'Friday')
    args,remaining=parser.parse_known_args()
    return subprocess.run([sys.executable,str(args.friday.resolve()/'scripts/verify_linux_container.py'),
                           *remaining]).returncode


if __name__=='__main__':raise SystemExit(main())
