import logging
from complex_app.main import main
import unittest

class TestMain(unittest.TestCase):
    def test_main_function(self):
        # This test is a bit high-level, as main is complex.
        # It mainly checks if the code runs without errors.
        with self.assertLogs("complex_app.main", level="INFO") as log_capture:
            main()

        # Assert that there were info logs
        self.assertGreaterEqual(len(log_capture.records), 1)
        for record in log_capture.records:
            self.assertEqual(record.levelno, logging.INFO)

if __name__ == '__main__':
    unittest.main()