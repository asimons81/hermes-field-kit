from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
SCRIPT = ROOT / "scripts" / "palette_to_theme.py"


class OmarchyThemeMakerContractTests(unittest.TestCase):
    def test_writes_are_confined_to_user_theme_directory(self):
        self.assertIn("~/.config/omarchy/themes/<slug>/", SKILL)
        self.assertIn("never edits stock themes under `/usr/share/omarchy/`", SKILL)

    def test_dry_run_precedes_writes(self):
        self.assertIn("--print", SKILL)
        self.assertIn("Dry-run", SKILL)

    def test_theme_application_requires_user_go_ahead(self):
        self.assertIn("omarchy theme set", SKILL)
        self.assertIn("only when the user asks", SKILL)

    def test_contrast_floor_is_documented(self):
        self.assertIn("3:1", SKILL)
        self.assertIn("contrast", SKILL.lower())

    def test_images_are_untrusted_pixel_data(self):
        self.assertIn("untrusted", SKILL.lower())
        self.assertIn("never instructions", SKILL)

    def test_script_exists_and_is_executable(self):
        self.assertTrue(SCRIPT.is_file())
        if sys.platform != "win32":
            # Windows checkouts carry no exec bit; only assert on POSIX.
            self.assertGreater(SCRIPT.stat().st_mode & 0o111, 0)

    def test_script_refuses_to_overwrite_without_force(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("--force", source)
        self.assertIn("refusing to overwrite", source)

    def test_script_rejects_symlinked_theme_paths(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("refusing to follow symlink", source)

    def test_script_skips_self_copy_of_staged_background(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("image.resolve() != bg_target.resolve()", source)

    def test_luminance_normalizes_by_weight_sum(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("weight_sum", source)
        # Uniform light-gray palette must classify as light, not dark.
        import importlib.util

        spec = importlib.util.spec_from_file_location("ptt", SCRIPT)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertGreater(mod.weighted_luminance(["#f0f0f0"] * 6), 0.9)

    def test_script_has_no_network_calls(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for forbidden in ("urllib", "requests", "http.client", "socket"):
            self.assertNotIn(forbidden, source, f"unexpected network import: {forbidden}")

    def test_behavior_cases_cover_trigger_behavior_and_safety(self):
        case_types = {case["type"] for case in CASES["cases"]}
        self.assertTrue({"positive-trigger", "negative-trigger", "behavior", "safety"}.issubset(case_types))
        ids = {case["id"] for case in CASES["cases"]}
        self.assertIn("safety-image-text-untrusted", ids)
        self.assertIn("safety-writes-contained", ids)


if __name__ == "__main__":
    unittest.main()
