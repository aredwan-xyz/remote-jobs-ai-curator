import json
import unittest
from unittest.mock import patch

import fetch_jobs as collector


class LocationTests(unittest.TestCase):
    def remotive_jobs(self, location):
        payload = {"jobs": [{"id": 1, "title": "Software Engineer", "company_name": "Example", "url": "https://example.com/job", "candidate_required_location": location}]}
        with patch.object(collector, "http_get", return_value=json.dumps(payload).encode()):
            return collector.fetch_remotive()

    def test_restricted_location_preserved(self):
        self.assertEqual(self.remotive_jobs("Canada only")[0]["location"], "Canada only")

    def test_unknown_is_not_worldwide(self):
        self.assertIn("Not specified", self.remotive_jobs("")[0]["location"])

    def test_explicit_worldwide_preserved(self):
        self.assertEqual(self.remotive_jobs("Worldwide")[0]["location"], "Worldwide")

    def test_empty_collection_does_not_overwrite(self):
        with patch.object(collector, "fetch_remoteok", return_value=[]), patch.object(collector, "fetch_remotive", return_value=[]), patch.object(collector, "fetch_wwr", return_value=[]), patch.object(collector, "fetch_jobicy", return_value=[]), patch.object(collector, "write_site_data") as write:
            with self.assertRaisesRegex(RuntimeError, "preserving"):
                collector.main()
            write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
