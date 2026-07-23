"""
Test suite for GitHub Actions workflow validation.
Verifies structure and requirements of .github/workflows/scraper.yml.
"""

import os
import re
import unittest
from pathlib import Path

# Resolve project root relative to this test file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "scraper.yml"

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class TestGitHubWorkflow(unittest.TestCase):
    """Automated validator for .github/workflows/scraper.yml."""

    @classmethod
    def setUpClass(cls):
        cls.workflow_path = WORKFLOW_PATH
        cls.file_exists = cls.workflow_path.is_file()
        if cls.file_exists:
            cls.raw_content = cls.workflow_path.read_text(encoding="utf-8")
        else:
            cls.raw_content = ""

        cls.parsed_yaml = None
        if cls.file_exists and HAS_YAML:
            try:
                cls.parsed_yaml = yaml.safe_load(cls.raw_content)
            except Exception:
                cls.parsed_yaml = None

    def test_workflow_file_exists(self):
        """Verify that .github/workflows/scraper.yml exists on disk."""
        self.assertTrue(
            self.file_exists,
            f"Workflow file does not exist at {self.workflow_path}"
        )

    def test_workflow_name(self):
        """Verify workflow name is 'Pokémon Price Scraper Cron'."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "name: Pokémon Price Scraper Cron",
            self.raw_content,
            "Workflow name 'Pokémon Price Scraper Cron' not found in scraper.yml"
        )
        if self.parsed_yaml:
            self.assertEqual(self.parsed_yaml.get("name"), "Pokémon Price Scraper Cron")

    def test_schedule_cron_trigger(self):
        """Verify schedule trigger contains cron '0 */6 * * *'."""
        self.assertTrue(self.file_exists)
        cron_pattern = r"cron:\s*['\"]0 \*/6 \* \* \*['\"]"
        self.assertIsNotNone(
            re.search(cron_pattern, self.raw_content),
            "Schedule cron expression '0 */6 * * *' not found in scraper.yml"
        )
        if self.parsed_yaml:
            on_block = self.parsed_yaml.get("on") or self.parsed_yaml.get(True) or {}
            schedule = on_block.get("schedule", [])
            cron_expressions = [item.get("cron") for item in schedule if isinstance(item, dict)]
            self.assertIn("0 */6 * * *", cron_expressions)

    def test_workflow_dispatch_trigger(self):
        """Verify workflow_dispatch trigger exists."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "workflow_dispatch:",
            self.raw_content.replace("\r\n", "\n"),
            "workflow_dispatch trigger not found in scraper.yml"
        )
        if self.parsed_yaml:
            on_block = self.parsed_yaml.get("on") or self.parsed_yaml.get(True) or {}
            self.assertIn("workflow_dispatch", on_block)

    def test_job_scrape_and_store(self):
        """Verify job scrape-and-store runs on ubuntu-latest."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "scrape-and-store:",
            self.raw_content,
            "Job 'scrape-and-store' not defined in scraper.yml"
        )
        self.assertIn(
            "runs-on: ubuntu-latest",
            self.raw_content,
            "Job 'scrape-and-store' does not specify 'runs-on: ubuntu-latest'"
        )
        if self.parsed_yaml:
            jobs = self.parsed_yaml.get("jobs", {})
            self.assertIn("scrape-and-store", jobs)
            job = jobs["scrape-and-store"]
            self.assertEqual(job.get("runs-on"), "ubuntu-latest")

    def test_step_checkout(self):
        """Verify checkout step uses actions/checkout@v4."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "actions/checkout@v4",
            self.raw_content,
            "Step using actions/checkout@v4 not found"
        )

    def test_step_setup_python(self):
        """Verify python setup step uses actions/setup-python@v5 with Python 3.11."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "actions/setup-python@v5",
            self.raw_content,
            "Step using actions/setup-python@v5 not found"
        )
        python_version_match = re.search(r"python-version:\s*['\"]?3\.11['\"]?", self.raw_content)
        self.assertIsNotNone(
            python_version_match,
            "python-version: '3.11' not found in setup-python step"
        )

    def test_step_install_dependencies(self):
        """Verify dependency installation step installs from scraper/requirements.txt."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "scraper/requirements.txt",
            self.raw_content,
            "Installation step referencing scraper/requirements.txt not found"
        )

    def test_step_pipeline_invocation(self):
        """Verify scraper pipeline execution python scraper/pipeline.py."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "python scraper/pipeline.py",
            self.raw_content,
            "Step running 'python scraper/pipeline.py' not found"
        )

    def test_env_secrets_passed(self):
        """Verify SUPABASE_URL and SUPABASE_KEY secrets are passed as env vars."""
        self.assertTrue(self.file_exists)
        self.assertIn(
            "SUPABASE_URL: ${{ secrets.SUPABASE_URL }}",
            self.raw_content,
            "SUPABASE_URL secret mapping not found in env block"
        )
        self.assertIn(
            "SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}",
            self.raw_content,
            "SUPABASE_KEY secret mapping not found in env block"
        )


if __name__ == "__main__":
    unittest.main()
