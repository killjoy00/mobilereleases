# Mobile portfolio CI audit — 2026-11-26

## What was measured

Read the latest up to 60 workflow runs per source repository, keeping records created in the preceding 14 days (as of 22:00 UTC). This is a **bounded recent sample**, not equal observation windows or a complete usage/billing report: for active repositories the cap covers only a portion of one day. Run elapsed time includes queuing and orchestration. For the representative successful runs below, use GitHub Jobs API start/completion timestamps and step durations to distinguish actual runner time from elapsed time. Sum job durations for runner minutes; parallel jobs do not add to wall-clock wait. Minutes are not dollar costs or GitHub billing multipliers.

| Repository | Representative evidence | Observed bottleneck / decision |
|---|---|---|
| Star/Run | [Playable PR](https://github.com/killjoy00/StarRun/actions/runs/45891460201): 17.3 runner min (10 jobs); [same-head branch push](https://github.com/killjoy00/StarRun/actions/runs/45891453075): 19.0 runner min. [Reliability audit](https://github.com/killjoy00/StarRun/actions/runs/45891459905): 17.3 runner min (18 jobs), ~32 min elapsed across two recent audit runs. | Multiple research matrices compete for runners. Add same-PR revision cancellation where absent; keep every current-revision assertion and existing classifier. Branch preview and PR merge-ref checks are not necessarily identical artifacts; do not remove them without establishing exact-source equivalence and preview requirements. |
| Pack One | [Backend gate](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/45896986974): 37.3 runner min (10 jobs). Corpus-readiness job 11.2 min, draft-run 9.9 min, corpus 6.1 min. | Expensive tests themselves dominate: 10.0, 8.3 and 4.8 min respectively in isolated domain tests. Preserve protected gates; investigate fixtures/queries separately rather than reducing required coverage. |
| Starport / Stuffy Land | [iOS CI](https://github.com/killjoy00/Starport/actions/runs/45891197877): 18.3 runner min. Simulator job 16.2 min; first install/launch step 8.7 min; Starport compile 1.3 min; Stuffy compile 1.9 min and launch 2.0 min. | Boot the selected iPhone during compilation, retain launch and survival checks, reuse exact simulator identity, cancel outdated PR revisions. |
| Gold Rush | [CI](https://github.com/killjoy00/GoldRush/actions/runs/45890950693): 11.9 runner min; compatibility screenshot job 7.3 min, boot/capture 5.7 min, compile 1.3 min. | Overlap simulator boot with compilation; retain App Review compatibility device, screenshot and launch delay. Push and PR triggers serve separate existing needs; don't remove branch builds by assumption. |
| Ultimate Tic/Tac/Toe | [Android CI](https://github.com/killjoy00/Ultttt/actions/runs/45422305520): 3.4 runner min, Gradle test/build 2.5 min. Recent 60 runs included 33 Android CI runs and 15 iOS CI runs. | Cancel superseded PR revisions, preserving each new revision, push, manual runs and lockfile writer. |
| EZ Trivia | [CI](https://github.com/killjoy00/EZTrivia/actions/runs/45891167269): 5.6 runner min; archive/build 3.1 min. | Already has cancellation and separate checks; do not remove unsigned archive or Android startup/Crashlytics checks. Investigate sharing exact Gradle intermediates later, not unverified artifact reuse. |
| Ministry | [Mobile CI](https://github.com/killjoy00/ministry/actions/runs/44629376942): 5.3 runner min, emulator job 2.4 min. | Already cancels old PR runs and scopes mobile checks. No safe high-impact change identified. |
| Food Finder | [iOS native validation](https://github.com/killjoy00/foodfinder/actions/runs/44432488210): 13.3 min elapsed, one recent native validation. | Too sparse for a recurring optimization claim. Do not introduce mobile release jobs solely for tracking. |
| TurnPro | 31 recent Turn Pro playtest runs, mean 2.2 min elapsed. | Low individual cost; preserve development checks. |

## Implementation

- [StarRun #101](https://github.com/killjoy00/StarRun/pull/101): same-PR cancellation in five expensive workflows; no matrix, assertion or event changes.
- [Ultttt #30](https://github.com/killjoy00/Ultttt/pull/30): same-PR cancellation across Android, iOS and backend CI; no cancellation of push or manual work.
- [Starport #23](https://github.com/killjoy00/Starport/pull/23): preboot while building, exact simulator identity and stale PR cancellation.
- [GoldRush #68](https://github.com/killjoy00/GoldRush/pull/68): overlap compatibility iPad boot and compile, always shut down the selected simulator.

CI was pending at the audit checkpoint. Measure the new successful job durations against the samples above; simulator runtime varies by host and cache state. Report actual elapsed and runner time rather than promising a fixed saving. A canceled superseded run is evidence of avoided stale work, not a reduction in the current revision's test coverage. No production release, new credentials, paid services, branch-rule exceptions or weakened release acceptance gates.

## Next measured work

Profile Pack One's two slow isolated backend domains before proposing a targeted performance change. Review Star/Run exact-commit branch/PR duplication in light of preview artifacts and merge-ref coverage. Collect multiple before/after samples before claiming sustained improvement. Release-request standardization and credential-expiry health checks are separate remaining work.
