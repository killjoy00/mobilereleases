# Mobile Releases

All ten apps, in one place. View current status directly here.

<!-- dashboard:start -->

**Last checked:** 2026-11-26 20:26 UTC · [Refresh history](https://github.com/killjoy00/mobilereleases/actions/workflows/mobile-release-status.yml)

### Store releases

| App | iOS public / ASC status | TestFlight | Apple review | Google Play production | Play internal testing |
|---|---|---|---|---|---|
| [Pack One](https://github.com/killjoy00/mtg-ev-analyzer) | 1.5 (US listing) | [1.4 (101135), in beta testing · Nov 19](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/44459578296) | Awaiting store check | [101224 submitted for review · Nov 26](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/45762020071); [public app owner-confirmed Nov 19](https://github.com/killjoy00/mtg-ev-analyzer/issues/575) | [101224 draft · Nov 26](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/45762020071); active tester version not checked |
| [EZ Trivia](https://github.com/killjoy00/EZTrivia) | 1.4 (US listing) | 1.4.0 (37) in beta testing [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | No pending version returned [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | Code 12 published on track [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809376) | Code 12 published on track [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809376) |
| [Gold Rush](https://github.com/killjoy00/GoldRush) | Awaiting store check | Awaiting store check | Awaiting store check | [No releases as of Sep 18](https://github.com/killjoy00/GoldRush/issues/53); fresh check needed | [1.5.1 (code 4) internal + closed testing · Sep 18](https://github.com/killjoy00/GoldRush/issues/53) |
| [Ultimate Tic/Tac/Toe](https://github.com/killjoy00/Ultttt) | Awaiting store check | 1.0 (100010) in beta testing [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | 1.0 waiting for review [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | Code 10 published on track [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809376) | Code 10 published on track [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809376) |
| [Star/Run](https://github.com/killjoy00/StarRun) | Awaiting store check | 1.4 (1044) in beta testing [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | 1.0 waiting for review [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | Code 14 published on track [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809376) | Code 14 draft, not available; Code 2 published on track [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809376) |
| [Ministry](https://github.com/killjoy00/ministry) | Awaiting store check | 1.0 (1005) in beta testing [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | 1.0 draft [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | Awaiting store check | Code 4 published on track [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809376) |
| [Starport](https://github.com/killjoy00/Starport) | Awaiting store check | 0.4.0 (100009) in beta testing [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | 1.0 draft [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | Not tracked | Not tracked |
| [Stuffy Land](https://github.com/killjoy00/Starport) | Awaiting store check | 0.1.4 (100009) in beta testing [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | 1.0 draft [2026-11-26](https://github.com/killjoy00/EZTrivia/actions/runs/45890809516) | Not tracked | Not tracked |
| [Food Finder](https://github.com/killjoy00/foodfinder) | Awaiting store check | Awaiting store check | Awaiting store check | Not tracked | Not tracked |
| [TurnPro](https://github.com/killjoy00/TurnPro) | Not tracked | Not tracked | Not tracked | Not tracked | Not tracked |

US Apple listings and dated provider checks are separate. Play published-on-track status may include staged or halted rollouts; it is not proof of universal public availability. Each dated result links to its evidence. **Awaiting store check** means evidence is missing; **Not tracked** means no configured route, not a claim the app does not exist.

### Development and next release

| App | iOS source | iOS request | Android source | Android request |
|---|---|---|---|---|
| Pack One | [1.6](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/mobile/store-release.json) | [Request file](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/.github/testflight-release-request.json) | [1.0](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/mobile/store-release.json) | [Request file](https://github.com/killjoy00/mtg-ev-analyzer/blob/main/.github/android-internal-release-request.json) |
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
| Pack One | [success](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/45754322805) (2026-11-26) | [success](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/43925032404) (2026-11-16) |
| EZ Trivia | [success](https://github.com/killjoy00/EZTrivia/actions/runs/44811434307) (2026-11-20) | Not verified |
| Gold Rush | [success](https://github.com/killjoy00/GoldRush/actions/runs/34381862332) (2026-09-09) | [success](https://github.com/killjoy00/GoldRush/actions/runs/35396057156) (2026-09-18) |
| Ultimate Tic/Tac/Toe | [success](https://github.com/killjoy00/EZTrivia/actions/runs/44330156632) (2026-11-18) | Route not verified |
| Star/Run | [success](https://github.com/killjoy00/EZTrivia/actions/runs/45715832907) (2026-11-25) | [success](https://github.com/killjoy00/EZTrivia/actions/runs/45715832919) (2026-11-25) |
| Ministry | [success](https://github.com/killjoy00/EZTrivia/actions/runs/44630462522) (2026-11-19) | [success](https://github.com/killjoy00/EZTrivia/actions/runs/44630462523) (2026-11-19) |
| Starport | [success](https://github.com/killjoy00/EZTrivia/actions/runs/42909547240) (2026-11-10) | Route not verified |
| Stuffy Land | [success](https://github.com/killjoy00/EZTrivia/actions/runs/42955989321) (2026-11-11) | Route not verified |
| Food Finder | Route not verified | Route not verified |
| TurnPro | Route not verified | Route not verified |

A successful workflow is not proof of store delivery; signed/uploaded, processing, review submission and tester availability require separate evidence.

<!-- dashboard:end -->

---

[Standard release instructions](mobile-releases/RELEASE_REQUESTS.md) · [App registry](mobile-releases/apps.json) · [Implementation tracker](https://github.com/killjoy00/EZTrivia/issues/190)

The dashboard automatically refreshes daily and after tracker code changes. It uses no store credentials and never starts a release.
