#!/usr/bin/env python3
"""Public, read-only release evidence. Never dispatches, builds or publishes."""
import argparse
import datetime as dt
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
import store_status

REGISTRY = Path(__file__).with_name("apps.json")
SHA = re.compile(r"[0-9a-f]{40}")
VERSION = re.compile(r"[0-9]+(?:\.[0-9]+){0,3}")
REPO = re.compile(r"killjoy00/[A-Za-z0-9_.-]+")
WORKFLOW = re.compile(r"[A-Za-z0-9_.-]+\.ya?ml")
BUNDLE = re.compile(r"[A-Za-z0-9_.-]+")
BRANCH = re.compile(r"[A-Za-z0-9_.-]+")
REQUEST = re.compile(r"\.github/[A-Za-z0-9_.-]+\.json")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
UNKNOWN = "Not verified"

def valid(pattern, value):
    return isinstance(value, str) and pattern.fullmatch(value) is not None

def read_json(url):
    # No credentials or write methods. Never print response bodies or exceptions.
    req = urllib.request.Request(url, headers={
        "User-Agent": "mobile-release-status-pilot/1",
        "Accept": "application/json",
    }, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            return json.loads(response.read(2_000_000))
    except (OSError, ValueError):
        return None

def validate_registry(registry):
    assert registry["schema_version"] == 1
    seen = set()
    for app in registry["apps"]:
        assert app["id"] not in seen
        seen.add(app["id"])
        assert valid(REPO, app["source"])
        for platform in ("ios", "android"):
            route = app[platform]
            if "workflow" in route:
                assert valid(REPO, route["repo"])
                assert valid(WORKFLOW, route["workflow"])
                assert valid(BRANCH, route.get("branch", "main"))
            if "request" in route:
                assert valid(REPO, route["repo"])
                assert valid(REQUEST, route["request"])
            if "bundle" in route:
                assert platform == "ios" and valid(BUNDLE, route["bundle"])
    return registry["apps"]

def head(repo, fetch):
    data = fetch(f"https://api.github.com/repos/{repo}/commits/main")
    sha = data.get("sha") if isinstance(data, dict) else None
    return f"[{sha[:8]}](https://github.com/{repo}/commit/{sha})" if valid(SHA, sha) else UNKNOWN

def workflow_run(route, fetch):
    if "workflow" not in route:
        return "Route not verified"
    repo, workflow = route["repo"], route["workflow"]
    query = urllib.parse.urlencode({"branch": route.get("branch", "main"), "per_page": 1})
    data = fetch(f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/runs?{query}")
    runs = data.get("workflow_runs") if isinstance(data, dict) else None
    if not runs or not isinstance(runs, list) or not isinstance(runs[0], dict):
        return UNKNOWN
    run = runs[0]
    run_id = run.get("id")
    if type(run_id) is not int or run_id <= 0:
        return UNKNOWN
    state = run.get("conclusion") or run.get("status")
    allowed = {"success", "failure", "cancelled", "skipped", "timed_out",
               "action_required", "neutral", "queued", "in_progress", "waiting",
               "requested", "pending", "completed", "stale", "startup_failure"}
    state = state if isinstance(state, str) and state in allowed else "unknown"
    stamp = run.get("updated_at")
    suffix = " (" + stamp[:10] + ")" if valid(DATE, stamp) else ""
    return f"[{state}](https://github.com/{repo}/actions/runs/{run_id}){suffix}"

def requested(app, route, fetch):
    """Report only allowlisted public request metadata, never raw request text."""
    if "request" not in route:
        return "No fixed request"
    repo, path = route["repo"], route["request"]
    link = f"https://github.com/{repo}/blob/main/{path}"
    data = fetch(f"https://raw.githubusercontent.com/{repo}/main/{path}")
    if not isinstance(data, dict):
        return UNKNOWN
    if data.get("repository", app["source"]) != app["source"]:
        return UNKNOWN
    if route.get("bundle") and data.get("bundleID", route["bundle"]) != route["bundle"]:
        return UNKNOWN
    version = data.get("version") or data.get("version_name")
    sha = data.get("sha") or data.get("source_sha")
    values = []
    if valid(VERSION, version):
        values.append(version)
    if valid(SHA, sha):
        values.append(sha[:8])
    code = data.get("version_code")
    if type(code) is int:
        code = str(code)
    if isinstance(code, str) and re.fullmatch(r"[0-9]{1,10}", code):
        values.append("code " + code)
    if data.get("release_status") == "draft":
        values.append("draft")
    return f"[{', '.join(values) if values else 'Request file'}]({link})"

def apple_public(route, fetch):
    bundle = route.get("bundle")
    if not bundle:
        return "Identity not verified"
    query = urllib.parse.urlencode({"bundleId": bundle, "country": "us", "entity": "software"})
    data = fetch(f"https://itunes.apple.com/lookup?{query}")
    results = data.get("results") if isinstance(data, dict) else None
    if not isinstance(results, list):
        return UNKNOWN
    matches = [r for r in results if isinstance(r, dict) and r.get("bundleId") == bundle]
    if len(matches) == 1 and valid(VERSION, matches[0].get("version")):
        return matches[0]["version"] + " (US listing)"
    # Absence is not proof of unpublished status.
    return UNKNOWN

def render(registry, fetch, now):
    apps = validate_registry(registry)
    heads = {repo: head(repo, fetch) for repo in dict.fromkeys(a["source"] for a in apps)}
    lines = ["# Mobile release status — read-only pilot", "",
             f"Checked at {now} UTC. A workflow result is NOT a signed build, upload, or store confirmation.", "",
             "| App | Development main | Platform | Requested candidate (not released) | Latest configured release workflow | Signed / uploaded | Testing | Submitted | Public |",
             "|---|---|---|---|---|---|---|---|---|"]
    for app in apps:
        for platform in ("ios", "android"):
            route = app[platform]
            candidate = requested(app, route, fetch)
            run = workflow_run(route, fetch)
            public = apple_public(route, fetch) if platform == "ios" else UNKNOWN
            lines.append(f"| {app['name']} | {heads[app['source']]} | {platform} | {candidate} | {run} | {UNKNOWN} | {UNKNOWN} | {UNKNOWN} | {public} |")
    lines += ["", "A shared publisher run's commit can belong to EZTrivia, not the app's binary.",
              "Development main is not the shipped commit. No authenticated store reads are wired in yet.",
              "Apple results describe only the US public listing; unknown does not mean unavailable.",
              "Failures and unavailable routes require investigation; do not infer release blockers from a workflow result alone."]
    return "\n".join(lines) + "\n"


START = "<!-- dashboard:start -->"
END = "<!-- dashboard:end -->"
DEV_VERSION = re.compile(r"[0-9]+(?:\.[0-9]+){0,3}(?:-alpha[0-9]+)?")
SOURCE_PATH = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*")

def read_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mobile-release-status/2"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            return response.read(2_000_000).decode("utf-8")
    except (OSError, ValueError):
        return None

def development(app, route, fetch_text):
    spec = route.get("development")
    if not spec or not valid(SOURCE_PATH, spec.get("path")) or ".." in spec["path"].split("/"):
        return UNKNOWN
    path, repo = spec["path"], app["source"]
    data = fetch_text(f"https://raw.githubusercontent.com/{repo}/main/{path}")
    if not isinstance(data, str):
        return UNKNOWN
    try:
        if "key" in spec:
            value = json.loads(data)
            for key in spec["key"].split("."):
                value = value[key]
        else:
            values = list(dict.fromkeys(re.findall(spec["pattern"], data)))
            index = spec.get("index")
            if len(values) != (1 if index is None else 2):
                return UNKNOWN
            value = values[0 if index is None else index]
    except (ValueError, TypeError, KeyError, IndexError, re.error):
        return UNKNOWN
    if not valid(DEV_VERSION, value):
        return UNKNOWN
    return f"[{value}](https://github.com/{repo}/blob/main/{path})"

def play_listing(route):
    package = route.get("package")
    if valid(BUNDLE, package):
        return f"[Store page](https://play.google.com/store/apps/details?id={package}) · unverified"
    return UNKNOWN

def homepage(registry, fetch, fetch_text, now):
    apps = validate_registry(registry)
    apple_doc = fetch(store_status.APPLE_URL)
    play_doc = fetch(store_status.PLAY_URL)
    lines = [
        f"**Last checked:** {now} UTC · [Refresh history](https://github.com/killjoy00/mobilereleases/actions/workflows/mobile-release-status.yml)",
        "", "### Store releases", "",
        "| App | iOS public / ASC status | TestFlight | Apple review | Google Play production | Play internal testing |",
        "|---|---|---|---|---|---|"]
    for app in apps:
        ios = app["ios"]
        values = store_status.cells(app, apple_doc, play_doc, apple_public(ios, fetch))
        lines.append(f"| [{app['name']}](https://github.com/{app['source']}) | " + " | ".join(values) + " |")
    lines += ["", "US Apple listings and dated provider checks are separate. Play published-on-track status may include staged or halted rollouts; it is not proof of universal public availability. Each dated result links to its evidence. **Awaiting store check** means evidence is missing; **Not tracked** means no configured route, not a claim the app does not exist.",
              "", "### Development and next release", "",
              "| App | iOS source | iOS request | Android source | Android request |",
              "|---|---|---|---|---|"]
    cache = {}
    def cached_text(url):
        if url not in cache:
            cache[url] = fetch_text(url)
        return cache[url]
    for app in apps:
        ios, android = app["ios"], app["android"]
        lines.append(f"| {app['name']} | {development(app, ios, cached_text)} | {requested(app, ios, fetch)} | {development(app, android, cached_text)} | {requested(app, android, fetch)} |")
    lines += ["", "Source versions are configuration values on main (possibly overridden by release workflows). A request is not a build or release.",
              "", "### Build and submission evidence", "",
              "| App | iOS release workflow | Android release workflow |",
              "|---|---|---|"]
    for app in apps:
        lines.append(f"| {app['name']} | {workflow_run(app['ios'], fetch)} | {workflow_run(app['android'], fetch)} |")
    lines += ["", "A successful workflow is not proof of store delivery; signed/uploaded, processing, review submission and tester availability require separate evidence."]
    return "\n".join(lines) + "\n"

def replace_dashboard(readme, report):
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must have exactly one dashboard block")
    before, tail = readme.split(START, 1)
    _, after = tail.split(END, 1)
    return before + START + "\n\n" + report.rstrip() + "\n\n" + END + after

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Read public GitHub and Apple listing APIs")
    parser.add_argument("--homepage", action="store_true", help="Render homepage dashboard")
    parser.add_argument("--update-readme", action="store_true", help="Update generated README section")
    args = parser.parse_args()
    if args.update_readme and not args.live:
        parser.error("--update-readme requires --live")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    fetch = read_json if args.live else lambda _: None
    if args.homepage or args.update_readme:
        report = homepage(registry, fetch, read_text if args.live else lambda _: None, now)
        if args.update_readme:
            path = REGISTRY.parent.parent / "README.md"
            path.write_text(replace_dashboard(path.read_text(encoding="utf-8"), report), encoding="utf-8")
        print(report, end="")
    else:
        print(render(registry, fetch, now), end="")

if __name__ == "__main__":
    main()
