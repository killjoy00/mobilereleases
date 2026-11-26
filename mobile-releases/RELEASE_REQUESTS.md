## Standard agent request

Accept natural language such as “Release Star/Run 1.3 to TestFlight and Google Play internal testing.” Resolve the app and platform in [apps.json](apps.json); read the current source/owner workflow and current request file before making changes. Normalize the intent:

- Application ID and platform(s); target separately for each platform (build only, private testing, submit for review, or production).
- Exact reviewed source commit SHA and requested marketing version for each platform; existing build/version allocator remains authoritative.
- Explicit owner authorization for each requested target; approval of a code PR or test upload is not permission for a production release.
- Current acceptance gates and exact artifact/build identity where applicable, especially production promotion.

Use the existing app-specific request-file PR or supported manual workflow only. Never fabricate a request or trigger a production promotion by guessing a version. For a route marked unverified or version-specific, inspect the current workflow and request first. If the connector cannot dispatch a manual-only workflow, report that limitation; do not invent an unsafe automatic trigger. Preserve Star/Run's draft default unless specifically authorized to distribute to internal testers. Follow Pack One's own runbook, gates and exact-artifact requirements. Use existing signing and production promotion paths unchanged.

Report source, signed build, upload, processing, testing track/group availability, review submission and public availability as separate stages with links, timestamps and evidence where available; state unknown where not verified. A workflow success or a store draft is never evidence of public availability. Sanitize public reports: no secrets, account identifiers, personal data, unreleased private operational detail, or raw store responses.

## Scope and rollout

All ten apps are registered, including two separate iOS identities sharing Starport's repo. EZTrivia and Star/Run are the first pilot; app-specific publishing infrastructure remains unchanged. Gold Rush's configured Apple bundle can be overridden, so its public identity is not assumed. Ultimate Tic/Tac/Toe's version-specific Android adapters need separate review. Food Finder and TurnPro are not assumed to have store-ready releases.

No new paid services or libraries. Run offline validation with `python3 -m unittest discover -s mobile-releases -p 'test_*.py'`. The dashboard workflow runs those tests before making a read-only refresh. Authenticated store read-back, credential health checks, production release routing and measured CI savings are follow-up work, not implemented by this pilot.

## Store status sources

The dashboard reads strictly validated public release-status snapshots from the repository that owns the app's credentials. EZTrivia serves its shared apps; Pack One and Gold Rush serve their own. No credential is copied to the tracker. Each provider observation has its own verification time and workflow link; evidence more than 36 hours old is marked stale. Gold Rush's configured default bundle must match the actual verified app record before reporting a version. Android status uses version codes because the direct store lifecycle API does not return a reliable marketing version name. Never infer one from source defaults or current requests.
