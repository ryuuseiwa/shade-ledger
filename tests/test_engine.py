import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine import MissionInput, build_prompt, local_summary, parse_mission, shade_score

VALID = {'title': 'Shade Hunt', 'mission': 'Walk. Notice shade.', 'steps': ['a', 'b', 'c'],
         'notice': ['x', 'y', 'z'], 'reflection': 'Where was it coolest?'}


class ParseMissionTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_mission(json.dumps(VALID)), VALID)

    def test_code_fence_and_extra_keys(self):
        raw = '```json\n' + json.dumps({**VALID, 'extra': 1}) + '\n```'
        self.assertEqual(parse_mission(raw), VALID)

    def test_missing_key(self):
        bad = {k: v for k, v in VALID.items() if k != 'reflection'}
        with self.assertRaises(ValueError):
            parse_mission(json.dumps(bad))

    def test_wrong_step_count(self):
        with self.assertRaises(ValueError):
            parse_mission(json.dumps({**VALID, 'steps': ['a', 'b']}))

    def test_non_string_notice(self):
        with self.assertRaises(ValueError):
            parse_mission(json.dumps({**VALID, 'notice': ['x', 'y', 3]}))

    def test_invalid_json(self):
        with self.assertRaises(json.JSONDecodeError):
            parse_mission('not json')


class ScoreTests(unittest.TestCase):
    def test_shade_score(self):
        self.assertEqual(shade_score(2, 4), 50)
        self.assertEqual(shade_score(1, 3), 33)
        self.assertIsNone(shade_score(5, 4))
        self.assertIsNone(shade_score(0, 0))
        self.assertIsNone(shade_score(-1, 4))

    def test_summary(self):
        self.assertIn('2 of 4', local_summary(2, 4, 3, 1))
        self.assertEqual(local_summary(5, 4, 0, 0), 'Add at least one valid observation.')


class PromptTests(unittest.TestCase):
    def test_prompt_includes_inputs(self):
        p = build_prompt(MissionInput(20, 'Public park', 'Slow stroll', 'Trees & biodiversity', 'Curious', 'Cool climate'))
        for s in ('20 minutes', 'Public park', 'Slow stroll', 'Trees & biodiversity', 'Curious', 'Cool climate'):
            self.assertIn(s, p)


if __name__ == '__main__':
    unittest.main()
