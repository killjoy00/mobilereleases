import json
import unittest
import status

class StatusTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(status.REGISTRY.read_text())
    def test_inventory(self):
        apps = status.validate_registry(self.registry)
        self.assertEqual(len(apps), 10)
        by_id = {a["id"]: a for a in apps}
        self.assertEqual(by_id["starport"]["source"], by_id["stuffy-land"]["source"])
        self.assertNotEqual(by_id["starport"]["ios"]["bundle"], by_id["stuffy-land"]["ios"]["bundle"])
    def test_run_success_does_not_infer_release(self):
        def fetch(url):
            if "/actions/" in url:
                return {"workflow_runs":[{"id":123,"conclusion":"success","head_sha":"a"*40}]}
            if "/commits/" in url:
                return {"sha":"b"*40}
            return None
        report = status.render(self.registry, fetch, "2026-11-26 00:00")
        self.assertIn("[success]", report)
        self.assertIn("Not verified | Not verified | Not verified | Not verified", report)
        self.assertNotIn("a"*40, report)
    def test_exact_apple_identity(self):
        route = {"bundle":"com.example.app"}
        self.assertEqual(status.apple_public(route, lambda _: {"results":[{"bundleId":"com.example.other","version":"1.0"}]}), status.UNKNOWN)
        self.assertEqual(status.apple_public(route, lambda _: {"results":[{"bundleId":"com.example.app","version":"1.2.3"}]}), "1.2.3 (US listing)")
        self.assertEqual(status.apple_public(route, lambda _: {"results":[]}), status.UNKNOWN)
    def test_unavailable(self):
        report = status.render(self.registry, lambda _: None, "2026-11-26 00:00")
        self.assertIn("TurnPro", report)
        self.assertIn("Route not verified", report)
        self.assertNotIn("[success]", report)
    def test_request_does_not_claim_release(self):
        app = {"source":"killjoy00/StarRun"}
        route = {"repo":"killjoy00/EZTrivia","request":".github/starrun-android-release-request.json"}
        data = {"source_sha":"a"*40,"version_name":"1.4.10","version_code":14,"release_status":"draft","release_notes":"NEVER PRINT"}
        value = status.requested(app, route, lambda _: data)
        self.assertIn("1.4.10, aaaaaaaa, code 14, draft", value)
        self.assertNotIn("NEVER PRINT", value)
        data["repository"] = "wrong"
        self.assertEqual(status.requested(app, route, lambda _: data), status.UNKNOWN)

    def test_homepage(self):
        report = status.homepage(self.registry, lambda _: None, lambda _: None, "2026-11-26 00:00")
        self.assertIn("### Store releases", report)
        self.assertIn("### Development and next release", report)
        for app in self.registry["apps"]:
            self.assertIn(app["name"], report)
        self.assertIn("not its availability", report)
        self.assertNotIn("TestFlight available", report)

    def test_development_version(self):
        app = {"source":"killjoy00/Starport"}
        route = {"development":{"path":"project.pbxproj","pattern":r"MARKETING_VERSION = ([0-9.]+);","index":1}}
        source = "MARKETING_VERSION = 0.4.0;\nMARKETING_VERSION = 0.4.0;\nMARKETING_VERSION = 0.1.4;"
        self.assertIn("[0.1.4]", status.development(app, route, lambda _: source))
        self.assertEqual(status.development(app, route, lambda _: source + "\nMARKETING_VERSION = 9.0;"), status.UNKNOWN)

    def test_update_readme_only_generated_block(self):
        source = "# Mobile Releases\n\n" + status.START + "\nold\n" + status.END + "\n\nFooter\n"
        self.assertEqual(status.replace_dashboard(source, "new\n"), "# Mobile Releases\n\n" + status.START + "\n\nnew\n\n" + status.END + "\n\nFooter\n")
        with self.assertRaises(ValueError):
            status.replace_dashboard("# missing markers", "new")

    def test_malformed_evidence(self):
        route = {"repo":"killjoy00/EZTrivia","workflow":"testflight.yml"}
        self.assertEqual(status.workflow_run(route, lambda _: {"workflow_runs":[{"id":"bad","conclusion":"success"}]}), status.UNKNOWN)
        self.assertEqual(status.head("killjoy00/EZTrivia", lambda _: {"sha":"bad"}), status.UNKNOWN)

if __name__ == "__main__":
    unittest.main()
