#!/usr/bin/env python3
"""
RankVerse Automated Quality Assurance & Security Test Suite (Section 17 & 18)
Run via: python3 test_rankverse.py -v
"""

import json
import os
import re
import unittest
import xml.etree.ElementTree as ET
import auto_fetch_resources as pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = os.path.join(BASE_DIR, "index.html")
DATA_JSON = os.path.join(BASE_DIR, "resources_data.json")
SITEMAP_XML = os.path.join(BASE_DIR, "sitemap.xml")
WORKFLOW_YML = os.path.join(BASE_DIR, ".github", "workflows", "daily_sync.yml")


class TestRankVersePlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pipeline.run_pipeline(validate_only=False)
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html = f.read()
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_01_json_schema_and_required_fields(self):
        """Verifies resources_data.json passes strict schema and required-field validation."""
        ok, errs = pipeline.validate_payload(self.data)
        self.assertTrue(ok, f"Schema validation failed: {errs}")
        self.assertEqual(self.data.get("schema_version"), "3.0")
        self.assertGreaterEqual(len(self.data.get("resources", [])), 1)
        self.assertGreaterEqual(len(self.data.get("notes", [])), 1)

    def test_02_no_duplicate_ids_in_data_or_dom(self):
        """Verifies zero duplicate resource/note IDs in JSON and zero duplicate element IDs in HTML."""
        res_ids = [r["id"] for r in self.data["resources"]]
        note_ids = [n["id"] for n in self.data["notes"]]
        self.assertEqual(len(res_ids), len(set(res_ids)), "Duplicate resource IDs found")
        self.assertEqual(len(note_ids), len(set(note_ids)), "Duplicate note IDs found")
        dom_ids = re.findall(r'\bid="([^"${]+)"', self.html)
        self.assertEqual(len(dom_ids), len(set(dom_ids)), "Duplicate DOM IDs found in index.html")

    def test_03_https_allowlist_enforcement(self):
        """Verifies verify_link_cyber_safety blocks HTTP, javascript:, and untrusted domains."""
        self.assertTrue(pipeline.verify_link_cyber_safety("https://ncert.nic.in/textbook/pdf/keph107.pdf"))
        self.assertTrue(pipeline.verify_link_cyber_safety("https://gpsc.gujarat.gov.in/"))
        self.assertTrue(pipeline.verify_link_cyber_safety("https://ssc.gov.in/"))
        self.assertFalse(pipeline.verify_link_cyber_safety("http://ncert.nic.in/textbook.pdf"))
        self.assertFalse(pipeline.verify_link_cyber_safety("javascript:alert(1)"))
        self.assertFalse(pipeline.verify_link_cyber_safety("https://malicious-phishing-site.example.com/file.pdf"))

    def test_04_recovery_blocks_invalid_generated_content(self):
        """Verifies validate_payload rejects malformed or untrusted entries before publication."""
        bad_payload = {
            "resources": [{
                "id": "bad-1",
                "title": "Untrusted Item",
                "exam": "JEE",
                "subject": "Physics",
                "format": "PDF",
                "directUrl": "http://untrusted.example.org/hack.exe",
                "source": "Unknown"
            }],
            "notes": []
        }
        ok, errs = pipeline.validate_payload(bad_payload)
        self.assertFalse(ok)
        self.assertTrue(any("Unsafe or non-allowlisted" in e for e in errs))

    def test_05_pipeline_idempotency(self):
        """Verifies running the pipeline twice does not duplicate records or delete existing content."""
        before_res_count = len(self.data["resources"])
        before_note_count = len(self.data["notes"])
        exit_code = pipeline.run_pipeline(validate_only=False)
        self.assertEqual(exit_code, 0)
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            after_data = json.load(f)
        self.assertEqual(len(after_data["resources"]), before_res_count)
        self.assertEqual(len(after_data["notes"]), before_note_count)

    def test_06_sitemap_and_generated_notes_consistency(self):
        """Verifies sitemap.xml is valid XML and every listed generated_notes file exists on disk."""
        self.assertTrue(os.path.exists(SITEMAP_XML))
        tree = ET.parse(SITEMAP_XML)
        root = tree.getroot()
        locs = [el.text for el in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertIn("https://tommyvercetti5700-code.github.io/RANKVERSE/", locs)
        for loc in locs:
            if "/generated_notes/" in loc:
                fn = loc.split("/generated_notes/")[-1]
                self.assertTrue(os.path.exists(os.path.join(BASE_DIR, "generated_notes", fn)), f"Missing generated note {fn}")

    def test_07_security_no_hardcoded_pins_or_placeholder_ads(self):
        """Verifies zero hard-coded admin PINs, zero ?owner= URL unlocks, and zero placeholder AdSense IDs."""
        self.assertNotIn("14071982", self.html)
        self.assertNotIn("params.get('owner')", self.html)
        self.assertNotIn("ca-pub-0000000000000000", self.html)

    def test_08_no_mandatory_login_wall(self):
        """Verifies Login Page (#flowPage1) is hidden and the step-by-step selector opens directly on Board Selection (#flowPage2)."""
        p1 = re.search(r'<div id="flowPage1" class="([^"]+)"', self.html)
        p2 = re.search(r'<div id="flowPage2" class="([^"]+)"', self.html)
        self.assertIsNotNone(p1)
        self.assertIsNotNone(p2)
        self.assertIn("hidden", p1.group(1).split())
        self.assertNotIn("hidden", p2.group(1).split())

    def test_09_honest_monetization_click_accounting(self):
        """Verifies recordAffiliateClick does not add simulated commissions to state.affiliateEarnings."""
        self.assertNotIn("state.affiliateEarnings += commissionAmount", self.html)
        self.assertIn("state.affiliateClicks += 1", self.html)

    def test_10_seo_and_multilingual_support(self):
        """Verifies canonical URL, meta description, JSON-LD, and English/Hindi/Gujarati language switcher."""
        self.assertIn('<link rel="canonical" href="https://tommyvercetti5700-code.github.io/RANKVERSE/">', self.html)
        self.assertIn('<meta name="description"', self.html)
        self.assertIn('"@type": "EducationalOrganization"', self.html)
        self.assertIn('id="langBtnEn"', self.html)
        self.assertIn('id="langBtnHi"', self.html)
        self.assertIn('id="langBtnGu"', self.html)

    def test_11_wcag_accessibility_and_mistake_review(self):
        """Verifies Skip-to-main-content link, prefers-reduced-motion, aria-live, and Adaptive Mistake Review."""
        self.assertIn('href="#mainContentArea"', self.html)
        self.assertIn('prefers-reduced-motion: reduce', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('id="filterMistakesOnlyBtn"', self.html)
        self.assertIn('id="openSupportAndTelemetryBtn"', self.html)

    def test_12_workflow_least_privilege_and_ci_gate(self):
        """Verifies GitHub Actions workflow uses least-privilege contents: write and runs tests before commit."""
        with open(WORKFLOW_YML, "r", encoding="utf-8") as f:
            yml = f.read()
        self.assertIn("contents: write", yml)
        self.assertIn("python3 test_rankverse.py", yml)


if __name__ == "__main__":
    unittest.main()
