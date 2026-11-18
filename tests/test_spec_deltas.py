"""Structural guard only; official OpenSpec validate remains authoritative."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / 'openspec/changes/bootstrap-smart-agriculture-platform/specs'

def orphan_requirements(text):
    in_delta = False
    errors = []
    for line in text.splitlines():
        if line.startswith('## '):
            in_delta = line in ('## ADDED Requirements', '## MODIFIED Requirements',
                               '## REMOVED Requirements', '## RENAMED Requirements')
        if line.startswith('### Requirement:') and not in_delta:
            errors.append(line)
    return errors

class DeltaLayoutTests(unittest.TestCase):
    def test_all_seventeen_capabilities_are_visible(self):
        paths = list(SPECS.glob('*/spec.md'))
        self.assertEqual(len(paths), 17)
        for path in paths:
            with self.subTest(capability=path.parent.name):
                self.assertIn('### Requirement:', path.read_text())
                self.assertEqual(orphan_requirements(path.read_text()), [])
    def test_original_missing_header_regression_is_detected(self):
        text = '## Purpose\nDescription\n### Requirement: Test\nMUST work'
        self.assertEqual(len(orphan_requirements(text)), 1)
    def test_notes_section_cannot_hide_requirements(self):
        text = '## ADDED Requirements\n### Requirement: Valid\n## Notes\n### Requirement: Hidden'
        self.assertEqual(orphan_requirements(text), ['### Requirement: Hidden'])

if __name__ == '__main__':
    unittest.main()
