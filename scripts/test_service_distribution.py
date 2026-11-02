#!/usr/bin/env python3
"""在临时文档仓库中核对公开下载同步，不修改真实部署配置。"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts/sync_service_tools.py"


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="friday-service-downloads-")
        self.guide = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.guide)], check=True)
        self.set_remote("https://github.com/lijunfeng722/friday-user-guide")

    def tearDown(self):
        self.temporary.cleanup()

    def set_remote(self, url):
        subprocess.run(["git", "-C", str(self.guide), "config", "remote.origin.url", url], check=True)

    def call(self, *args):
        result = subprocess.run([sys.executable, str(SYNC), "--guide", str(self.guide), *args],
                                text=True, capture_output=True, timeout=10)
        return result.returncode, json.loads(result.stdout)

    def test_bundle_drift_is_detected_and_local_configuration_is_untouched(self):
        private = self.guide / "services.local.json"
        private.write_text('{"example":"SYNTHETIC-private-configuration"}')
        before = private.read_bytes()
        self.assertEqual(self.call()[0], 0)
        self.assertEqual(self.call("--check")[0], 0)
        start = self.guide / "docs/assets/scripts/start-friday.sh"
        start.write_bytes(start.read_bytes() + b"\n# SYNTHETIC\n")
        self.assertEqual(self.call("--check")[0], 1)
        self.assertNotEqual(start.read_bytes(), (ROOT / "start-friday.sh").read_bytes())
        self.assertEqual(private.read_bytes(), before)
        self.assertEqual(self.call()[0], 0)
        self.assertEqual(start.read_bytes(), (ROOT / "start-friday.sh").read_bytes())
        self.assertEqual(private.read_bytes(), before)

    def test_unmanaged_repository_is_not_written(self):
        self.set_remote("https://github.com/home-assistant/core")
        self.assertEqual(self.call()[0], 1)
        self.assertFalse((self.guide / "docs").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
