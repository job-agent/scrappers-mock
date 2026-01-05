"""Quality tests for type checking validation.

These tests verify that mypy type checking passes for all packages
in scrappers-mock.
"""

import subprocess
import sys
from pathlib import Path

import pytest


pytestmark = pytest.mark.quality


class TestTypeChecking:
    """Verify type checking passes for all packages."""

    def _run_mypy(self, package_path: Path, package_name: str) -> tuple[int, str, str]:
        """Run mypy on a package and return (returncode, stdout, stderr)."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                str(package_path),
                "--ignore-missing-imports",
                "--no-error-summary",
            ],
            capture_output=True,
            text=True,
            cwd=package_path.parent.parent,
        )
        return result.returncode, result.stdout, result.stderr

    def _check_mypy_available(self) -> bool:
        """Check if mypy is available in the environment."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "mypy", "--version"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _format_mypy_errors(self, stdout: str, stderr: str) -> str:
        """Format mypy output into actionable error message."""
        output_lines = []
        if stdout.strip():
            output_lines.append("Type errors found:")
            error_lines = stdout.strip().split("\n")
            for line in error_lines[:20]:
                output_lines.append(f"  {line}")
            if len(error_lines) > 20:
                output_lines.append(f"  ... and {len(error_lines) - 20} more errors")
        if stderr.strip():
            output_lines.append(f"mypy stderr: {stderr.strip()}")
        return "\n".join(output_lines)

    @pytest.fixture
    def mypy_available(self) -> bool:
        """Check if mypy is installed and available."""
        return self._check_mypy_available()

    @pytest.mark.parametrize(
        "package_dir_name,source_subdir",
        [
            ("scrapper-service", "scrapper_service"),
        ],
        ids=[
            "scrapper-service",
        ],
    )
    def test_package_type_checking_passes(
        self,
        packages_dir: Path,
        package_dir_name: str,
        source_subdir: str,
        mypy_available: bool,
    ) -> None:
        """Type checking passes for the package with no errors."""
        if not mypy_available:
            pytest.skip(
                "mypy not available. Install with: pip install mypy\n"
                "Hint: mypy is required for type checking quality tests."
            )

        source_dir = packages_dir / package_dir_name / "src" / source_subdir
        if not source_dir.exists():
            pytest.skip(f"Source directory not found: {source_dir}")

        returncode, stdout, stderr = self._run_mypy(source_dir, source_subdir)

        assert returncode == 0, (
            f"Type checking failed for {package_dir_name}:\n"
            f"{self._format_mypy_errors(stdout, stderr)}\n\n"
            f"Run 'mypy {source_dir}' for full output."
        )


class TestMypyConfiguration:
    """Verify mypy can be run and configured correctly."""

    def test_mypy_is_installed(self) -> None:
        """mypy is installed and can be invoked."""
        result = subprocess.run(
            [sys.executable, "-m", "mypy", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip("mypy is not installed. Install with: pip install mypy")

        version_output = result.stdout.strip()
        assert "mypy" in version_output.lower(), f"Unexpected mypy version output: {version_output}"
