# Mobile Releases

All ten apps, in one place. View current status directly here.

<!-- dashboard:start -->

**Last checked:** 2026-11-26 19:45 UTC · [Refresh history](https://github.com/killjoy00/mobilereleases/actions/workflows/mobile-release-status.yml)

### Store releases

| App | iOS public (US) | TestFlight | Google Play public | Play testing |
|---|---|---|---|---|
| [Pack One](https://github.com/killjoy00/mtg-ev-analyzer) | 1.5 (US listing) | Not verified | [Store page](https://play.google.com/store/apps/details?id=pro.packone.app) · unverified | Not verified |
| [EZ Trivia](https://github.com/killjoy00/EZTrivia) | 1.4 (US listing) | Not verified | [Store page](https://play.google.com/store/apps/details?id=com.rsm.eztrivia) · unverified | Not verified |
| [Gold Rush](https://github.com/killjoy00/GoldRush) | Identity not verified | Not verified | [Store page](https://play.google.com/store/apps/details?id=com.killjoy00.goldrush) · unverified | Not verified |
| [Ultimate Tic/Tac/Toe](https://github.com/killjoy00/Ultttt) | Not verified | Not verified | [Store page](https://play.google.com/store/apps/details?id=com.killjoy00.ultttt) · unverified | Not verified |
| [Star/Run](https://github.com/killjoy00/StarRun) | Not verified | Not verified | [Store page](https://play.google.com/store/apps/details?id=com.rsm.starrun) · unverified | Not verified |
| [Ministry](https://github.com/killjoy00/ministry) | Not verified | Not verified | [Store page](https://play.google.com/store/apps/details?id=org.killjoy00.ministry) · unverified | Not verified |
| [Starport](https://github.com/killjoy00/Starport) | Not verified | Not verified | Not verified | Not verified |
| [Stuffy Land](https://github.com/killjoy00/Starport) | Not verified | Not verified | Not verified | Not verified |
| [Food Finder](https://github.com/killjoy00/foodfinder) | Not verified | Not verified | Not verified | Not verified |
| [TurnPro](https://github.com/killjoy00/TurnPro) | Identity not verified | Not verified | Not verified | Not verified |

Apple public versions come from exact-bundle lookup. Play links identify the app, not its availability. Testing and Play production versions require authenticated store read-back. **Not verified** means unknown, not unreleased.

### Development and next release

| App | iOS source | iOS request | Android source | Android request |
|---|---|---|---|---|
| Pack One | [1.5](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/mobile/store-release.json) | [Request file](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/.github/testflight-release-request.json) | [1.0](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/mobile/store-release.json) | [Request file](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/.github/android-internal-release-request.json) |
| EZ Trivia | [1.4.0](https://github.com/killjoy00/EZTrivia/blob/main/EZTrivia.xcodeproj/project.pbxproj) | [1.4.0](https://github.com/killjoy00/EZTrivia/blob/main/.github/eztrivia-testflight-request.json) | [1.0.0-alpha01](https://github.com/killjoy00/EZTrivia/blob/main/android/app/build.gradle.kts) | No fixed request |
| Gold Rush | [1.03](https://github.com/killjoy00/GoldRush/blob/main/App/GoldRush.xcodeproj/project.pbxproj) | No fixed request | [1.5.1](https://github.com/killjoy00/GoldRush/blob/main/Android/app/build.gradle.kts) | No fixed request |
| Ultimate Tic/Tac/Toe | [1.0](https://github.com/killjoy00/Ultttt/blob/main/project.yml) | [1.0, 215697c6](https://github.com/killjoy00/EZTrivia/blob/main/.github/ultttt-testflight-request.json) | [1.1.1](https://github.com/killjoy00/Ultttt/blob/main/android/app/build.gradle.kts) | No fixed request |
| Star/Run | [1.3](https://github.com/killjoy00/StarRun/blob/main/export_presets.cfg) | [1.4, 2da45925](https://github.com/killjoy00/EZTrivia/blob/main/.github/starrun-release-request.json) | [1.3](https://github.com/killjoy00/StarRun/blob/main/export_presets.cfg) | [1.4.10, 2da45925, code 14, draft](https://github.com/killjoy00/EZTrivia/blob/main/.github/starrun-android-release-request.json) |
| Ministry | [0.1.0](https://github.com/killjoy00/ministry/blob/main/export_presets.cfg) | [1.0, 5dd23f4b](https://github.com/killjoy00/EZTrivia/blob/main/.github/ministry-testflight-request.json) | [0.1.0](https://github.com/killjoy00/ministry/blob/main/export_presets.cfg) | [0.1.3, 5dd23f4b, code 4](https://github.com/killjoy00/EZTrivia/blob/main/.github/ministry-android-release-request.json) |
| Starport | [0.4.0](https://github.com/killjoy00/Starport/blob/main/Starport.xcodeproj/project.pbxproj) | [0.4.0, 346416fe](https://github.com/killjoy00/EZTrivia/blob/main/.github/starport-release-request.json) | Not verified | No fixed request |
| Stuffy Land | [0.1.4](https://github.com/killjoy00/Starport/blob/main/Starport.xcodeproj/project.pbxproj) | [0.1.4, eece4872](https://github.com/killjoy00/EZTrivia/blob/main/.github/stuffyland-release-request.json) | Not verified | No fixed request |
| Food Finder | [1.0.0](https://github.com/killjoy00/foodfinder/blob/main/mobile/app.json) | No fixed request | Not verified | No fixed request |
| TurnPro | Not verified | No fixed request | Not verified | No fixed request |

Source versions are configuration values on main (possibly overridden by release workflows). A request is not a build or release.

### Build and submission evidence

| App | iOS release workflow | Android release workflow |
|---|---|---|
| Pack One | Not verified | Not verified |
| EZ Trivia | Not verified | Not verified |
| Gold Rush | Not verified | Not verified |
| Ultimate Tic/Tac/Toe | Not verified | Route not verified |
| Star/Run | Not verified | Not verified |
| Ministry | Not verified | Not verified |
| Starport | Not verified | Route not verified |
| Stuffy Land | Not verified | Route not verified |
| Food Finder | Route not verified | Route not verified |
| TurnPro | Route not verified | Route not verified |

A successful workflow is not proof of store delivery; signed/uploaded, processing, review submission and tester availability require separate evidence.

<!-- dashboard:end -->

---

[Standard release instructions](mobile-releases/RELEASE_REQUESTS.md) · [App registry](mobile-releases/apps.json) · [Implementation tracker](https://github.com/killjoy00/EZTrivia/issues/190)

The dashboard automatically refreshes daily and after tracker code changes. It uses no store credentials and never starts a release.
