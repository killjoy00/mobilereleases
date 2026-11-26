import json
import unittest
import status
import store_status

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
        self.assertIn("not a claim the app does not exist", report)
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

    def test_store_evidence_distinguishes_draft_and_published(self):
        app = {"id":"star-run","ios":{"bundle":"com.rsm.starrun"},"android":{"package":"com.rsm.starrun"}}
        doc = {"schema_version":1,"checked_at":"2026-11-26T12:00:00Z","run_id":"123","apps":{"star-run":{"package":"com.rsm.starrun","tracks":{"production":{"result":"ok","releases":[]},"internal":{"result":"ok","releases":[{"state":"DRAFT","codes":["14"]},{"state":"PUBLISHED","codes":["2"]}]}}}}}
        _, _, _, production, testing = store_status.cells(app,None,doc,status.UNKNOWN)
        self.assertIn("No active releases returned",production)
        self.assertIn("Code 14 draft, not available",testing)
        self.assertIn("Code 2 published on track",testing)
        doc["apps"]["star-run"]["package"]="wrong"
        self.assertIsNone(store_status.play(doc,"star-run","com.rsm.starrun","internal"))

    def test_apple_beta_and_review_separate(self):
        doc = {"schema_version":1,"checked_at":"2026-11-26T12:00:00Z","run_id":"123","apps":{"star-run":{"bundle":"com.rsm.starrun","result":"ok","builds":[{"version":"1.4","build":"1100","processing":"PROCESSING","expired":False},{"version":"1.3","build":"1099","processing":"VALID","internal":"IN_BETA_TESTING","expired":False}],"versions":[{"version":"1.2","state":"READY_FOR_DISTRIBUTION"},{"version":"1.3","state":"IN_REVIEW"}]}}}
        live,beta,review = store_status.apple(doc,"star-run","com.rsm.starrun")
        self.assertIn("1.2 ready for distribution (ASC)",live)
        self.assertIn("1.3 (1099) in beta testing",beta)
        self.assertIn("1.4 (1100) processing",beta)
        self.assertIn("1.3 in review",review)

    def test_independent_snapshot_provenance_and_staleness(self):
        doc={"schema_version":1,"checked_at":"2026-11-26T12:00:00Z","run_id":"123","apps":{"pack-one":{"bundle":"pro.packone.app"}}}
        row, label=store_status.source(doc,"pack-one","bundle","pro.packone.app","killjoy00/mtg-ev-analyzer","2026-11-28 12:00")
        self.assertEqual(row["bundle"],"pro.packone.app")
        self.assertIn("stale",label)
        self.assertIn("killjoy00/mtg-ev-analyzer/actions/runs/123",label)
        self.assertEqual(store_status.source(doc,"pack-one","bundle","pro.packone.app","untrusted/repo"),(None,None))
        self.assertEqual(store_status.source(doc,"pack-one","bundle","pro.packone.app","killjoy00/mtg-ev-analyzer","2026-11-25 12:00"),(None,None))
        self.assertIsNone(store_status.snapshot_url("untrusted/repo","apple"))

    def test_checked_but_not_live_or_unavailable(self):
        apple_doc={"schema_version":1,"checked_at":"2026-11-26T12:00:00Z","run_id":"123","apps":{"star-run":{"bundle":"com.rsm.starrun","result":"ok","builds":[],"versions":[{"version":"1.0","state":"WAITING_FOR_REVIEW"}]}}}
        public,beta,review=store_status.apple(apple_doc,"star-run","com.rsm.starrun")
        self.assertIn("No ready-for-distribution version returned",public)
        self.assertIn("1.0 waiting for review",review)
        play_doc={"schema_version":1,"checked_at":"2026-11-26T12:00:00Z","run_id":"124","apps":{"ministry":{"package":"org.killjoy00.ministry","tracks":{"production":{"result":"unavailable","releases":[]}}}}}
        self.assertIn("Track check unavailable",store_status.play(play_doc,"ministry","org.killjoy00.ministry","production"))

    def test_packone_dedicated_issue_feed(self):
        apple={"schema_version":1,"checked_at":"2026-11-26T12:00:00Z","run_id":"123","apps":{"pack-one":{"bundle":"pro.packone.app"}}}
        body="<!-- portfolio-status:start -->\n"+chr(96)*3+"json\n"+json.dumps({"apple":apple})+"\n"+chr(96)*3+"\n<!-- portfolio-status:end -->"
        issue={"number":1867,"body":body}
        def fetch(url):
            self.assertEqual(url,store_status.PACKONE_ISSUE_URL)
            return issue
        self.assertEqual(store_status.snapshots("killjoy00/mtg-ev-analyzer",fetch),(apple,None))
        self.assertEqual(store_status.issue_snapshots({"number":1866,"body":body}),(None,None))
        self.assertEqual(store_status.issue_snapshots({"number":1867,"body":body+body}),(None,None))

    def test_compact_overview_preserves_release_distinctions(self):
        stamp = " [2026-11-26 20:24 UTC](https://github.com/killjoy00/EZTrivia/actions/runs/123)"
        self.assertEqual(status.compact_cell("1.4 (1044) in beta testing"+stamp),"1.4 (1044)")
        self.assertEqual(status.compact_cell("Code 14 draft, not available; Code 2 published on track"+stamp),"Build 14 (draft); Build 2")
        self.assertEqual(status.compact_cell("1.0 waiting for review"+stamp),"1.0 · Waiting")
        self.assertEqual(status.compact_cell("No ready-for-distribution version returned"+stamp),"Not live")
        self.assertEqual(status.compact_cell("Track check unavailable"+stamp),"Check needed")
        self.assertEqual(status.compact_cell("Not tracked"),"—")
        self.assertEqual(status.compact_cell("1.5 (US listing)"),"1.5")
        self.assertEqual(status.compact_cell("1.4 (1044) in beta testing"+stamp.replace("UTC]","UTC · stale]")),"1.4 (1044) (stale)")
        self.assertIn("Nov 19",status.compact_cell(store_status.HISTORICAL["pack-one"]["beta"]))

    def test_overview_hides_technical_tables_by_default(self):
        report=status.homepage(self.registry,lambda _:None,lambda _:None,"2026-11-26 00:00")
        visible,details=report.split("<details>",1)
        self.assertEqual(visible.count("| App |"),1)
        self.assertNotIn("source |",visible)
        self.assertNotIn("request |",visible)
        self.assertNotIn("actions/runs/",visible)
        self.assertIn("Technical details and release evidence",details)
        self.assertIn("### Development and next release",details)
        self.assertIn("### Build and submission evidence",details)
        self.assertTrue(report.rstrip().endswith("</details>"))

    def test_ministry_owner_confirmation_is_fallback_only(self):
        app=next(a for a in self.registry["apps"] if a["id"]=="ministry")
        doc={"schema_version":1,"checked_at":"2026-11-26T20:24:00Z","run_id":"124","apps":{"ministry":{"package":"org.killjoy00.ministry","tracks":{"production":{"result":"unavailable","releases":[]},"internal":{"result":"ok","releases":[{"state":"PUBLISHED","codes":["4"]}]}}}}}
        result=store_status.cells(app,None,doc,status.UNKNOWN,"2026-11-26 21:00")
        self.assertEqual(result[3],"Not live (owner confirmed Nov 26)")
        self.assertIn("Code 4 published",result[4])
        doc["apps"]["ministry"]["tracks"]["production"]={"result":"ok","releases":[{"state":"PUBLISHED","codes":["5"]}]}
        result=store_status.cells(app,None,doc,status.UNKNOWN,"2026-11-26 21:00")
        self.assertIn("Code 5 published",result[3])
        self.assertNotIn("owner confirmed",result[3])

    def test_malformed_evidence(self):
        route = {"repo":"killjoy00/EZTrivia","workflow":"testflight.yml"}
        self.assertEqual(status.workflow_run(route, lambda _: {"workflow_runs":[{"id":"bad","conclusion":"success"}]}), status.UNKNOWN)
        self.assertEqual(status.head("killjoy00/EZTrivia", lambda _: {"sha":"bad"}), status.UNKNOWN)

if __name__ == "__main__":
    unittest.main()
