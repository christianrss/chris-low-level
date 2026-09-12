from __future__ import annotations

import sys
import tempfile
import unittest
import shutil
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import cycle_contract_check
import day_contract_check
import depth_manifest
import depth_quality_check
import pedagogy_check_unified
import run_day_tests
import run_depth_mutants


FIXTURES = ROOT / "tests" / "fixtures" / "depth_first"
VALID = FIXTURES / "valid"


class DepthFirstContractTests(unittest.TestCase):
    def test_yaml_fallback_reads_nested_contract(self) -> None:
        with patch.object(depth_manifest, "yaml", None):
            data = depth_manifest.load_yaml(VALID / "ASSESSMENT.yaml")
        self.assertEqual(data["profile"], "depth_first")
        self.assertEqual(len(data["milestones"]), 6)
        self.assertEqual(data["rubric"]["categories"]["implementation"], 30)

    def test_yaml_fallback_reads_track_profiles(self) -> None:
        with patch.object(depth_manifest, "yaml", None):
            data = depth_manifest.load_yaml(
                ROOT / "openspec" / "specs" / "day-contract" / "tracks.yaml"
            )
        self.assertEqual(data["tiers"]["depth_first"]["max_modules"], 1)
        self.assertIn("rust", data["curriculum_lanes"]["systems"]["paths"])
        self.assertIn("2026-09-06", data["tiers"]["tier_a"]["days"])

    def test_valid_day_contract_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw)
            learning_paths = temp / "LEARNING_PATHS.md"
            module_map = temp / "module_project_map.py"
            learning_paths.write_text("valid/systems/deep_fixture\n", encoding="utf-8")
            module_map.write_text("", encoding="utf-8")
            with (
                patch.object(day_contract_check, "LEARNING_PATHS", learning_paths),
                patch.object(day_contract_check, "MODULE_MAP", module_map),
            ):
                errors, _warnings = day_contract_check.check_day(VALID)
        self.assertEqual(errors, [])

    def test_valid_assessment_fixture(self) -> None:
        def fake_sloc(path: Path) -> int:
            return 300 if "solutions" in path.parts else 0

        with patch.object(depth_quality_check, "substantive_lines", fake_sloc):
            errors = depth_quality_check.check_assessment(VALID)
        self.assertEqual(errors, [])

    def test_declared_mutants_are_executed(self) -> None:
        self.assertEqual(run_depth_mutants.run_mutants(VALID), [])

    def test_numbered_padding_is_rejected(self) -> None:
        body = (FIXTURES / "bad_padding" / "TEORIA_PASSO_A_PASSO.md").read_text(
            encoding="utf-8"
        )
        self.assertTrue(pedagogy_check_unified.has_numbered_padding(body))

    def test_planned_cycle_covers_every_lane(self) -> None:
        errors, _warnings = cycle_contract_check.check_cycle(
            ROOT
            / "openspec"
            / "specs"
            / "day-contract"
            / "cycles"
            / "depth-core-01.yaml"
        )
        self.assertEqual(errors, [])

    def test_python_runner_executes_every_test_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw)
            module = temp / "days" / "2099-01-01" / "systems" / "runner"
            tests = module / "starter" / "tests"
            tests.mkdir(parents=True)
            (tests / "test_01_pass.py").write_text("", encoding="utf-8")
            (tests / "test_02_fail.py").write_text(
                "raise SystemExit(3)\n", encoding="utf-8"
            )
            with patch.object(run_day_tests, "ROOT", temp):
                ok, message = run_day_tests.run_module(module, "starter")
        self.assertFalse(ok)
        self.assertIn("test_02_fail.py failed", message)

    def test_skip_detection_distinguishes_not_run(self) -> None:
        self.assertTrue(run_day_tests.is_skipped_result("no automated runner (skipped)"))
        self.assertFalse(run_day_tests.is_skipped_result("ctest OK"))

    def test_two_projects_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            copied = Path(raw) / "valid"
            shutil.copytree(VALID, copied)
            second = copied / "systems" / "second_project"
            second.mkdir(parents=True)
            (second / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").write_text(
                "# Resolution\n", encoding="utf-8"
            )
            with tempfile.TemporaryDirectory() as refs:
                learning_paths = Path(refs) / "LEARNING_PATHS.md"
                module_map = Path(refs) / "module_project_map.py"
                learning_paths.write_text(
                    "valid/systems/deep_fixture\nvalid/systems/second_project\n",
                    encoding="utf-8",
                )
                module_map.write_text("", encoding="utf-8")
                with (
                    patch.object(day_contract_check, "LEARNING_PATHS", learning_paths),
                    patch.object(day_contract_check, "MODULE_MAP", module_map),
                ):
                    errors, _warnings = day_contract_check.check_day(copied)
        self.assertTrue(any("allows <= 1 modules" in error for error in errors))

    def test_pre_resolved_starter_is_rejected(self) -> None:
        def same_sloc(_path: Path) -> int:
            return 300

        with patch.object(depth_quality_check, "substantive_lines", same_sloc):
            errors = depth_quality_check.check_assessment(VALID)
        self.assertTrue(any("authored production delta" in error for error in errors))
        self.assertTrue(any("starter contains" in error for error in errors))

    def test_incomplete_cycle_is_rejected(self) -> None:
        source = (
            ROOT
            / "openspec"
            / "specs"
            / "day-contract"
            / "cycles"
            / "depth-core-01.yaml"
        ).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            broken = Path(raw) / "broken.yaml"
            broken.write_text(
                source.replace("id: depth-core-01", "id: broken").replace(
                    "primary_lane: tooling", "primary_lane: systems"
                ),
                encoding="utf-8",
            )
            errors, _warnings = cycle_contract_check.check_cycle(broken)
        self.assertTrue(any("missing required lanes: tooling" in error for error in errors))

    def test_expected_failure_rejects_passing_starter(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            day = root / "days" / "2099-01-01"
            module = day / "systems" / "runner"
            tests = module / "starter" / "tests"
            tests.mkdir(parents=True)
            (module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").write_text(
                "# Resolution\n", encoding="utf-8"
            )
            (tests / "test_pass.py").write_text("", encoding="utf-8")
            (day / "day.contract.yaml").write_text(
                "profile: depth_first\n", encoding="utf-8"
            )
            (day / "ASSESSMENT.yaml").write_text(
                "starter_expected_failures: [systems/runner]\n", encoding="utf-8"
            )
            argv = [
                "run_day_tests.py",
                "--day",
                "2099-01-01",
                "--mode",
                "starter",
                "--expect-fail",
            ]
            with (
                patch.object(run_day_tests, "ROOT", root),
                patch.object(sys, "argv", argv),
            ):
                with redirect_stdout(io.StringIO()):
                    result = run_day_tests.main()
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
