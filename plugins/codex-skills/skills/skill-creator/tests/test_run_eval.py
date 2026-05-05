from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.run_eval import parse_trigger_result, resolve_trigger_result


class TriggerResultParsingTest(unittest.TestCase):
    def test_output_artifact_wins_over_later_stdout_noise(self) -> None:
        output_text = '{"trigger": true}\n'
        stdout_text = 'INFO: echoed prompt {"trigger": false}\n{"trigger": false}'

        self.assertTrue(resolve_trigger_result(output_text, stdout_text))

    def test_stdout_is_used_when_output_artifact_is_missing(self) -> None:
        output_text = ""
        stdout_text = '{"trigger": true}\n'

        self.assertTrue(resolve_trigger_result(output_text, stdout_text))

    def test_noisy_inline_fragments_are_rejected(self) -> None:
        noisy_text = 'INFO: prompt echo {"trigger": true}\nINFO: later noise {"trigger": false}'

        self.assertIsNone(parse_trigger_result(noisy_text))

    def test_raises_when_no_trigger_result_exists(self) -> None:
        with self.assertRaises(ValueError):
            resolve_trigger_result("", 'INFO: prompt echo {"trigger": true}\nINFO: later noise {"trigger": false}')


if __name__ == "__main__":
    unittest.main()
