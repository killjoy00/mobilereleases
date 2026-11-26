"""Turn sanitized, dated store observations into dashboard cells.

Never treat a build/request, draft, or approved-not-published release as live.
Only the publisher-produced GET snapshots establish current store lifecycle.
"""
import re
import json
import datetime as dt

APPLE_URL="https://raw.githubusercontent.com/killjoy00/EZTrivia/main/release-status/apple.json"
PLAY_URL="https://raw.githubusercontent.com/killjoy00/EZTrivia/main/release-status/play.json"
TRUSTED_PUBLISHERS={"killjoy00/EZTrivia","killjoy00/mtg-ev-analyzer","killjoy00/GoldRush"}

def snapshot_url(repo, platform):
    if repo in TRUSTED_PUBLISHERS and platform in ("apple","play"):
        return f"https://raw.githubusercontent.com/{repo}/main/release-status/{platform}.json"
    return None
STAMP=re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
VERSION=re.compile(r"[0-9]+(?:\.[0-9]+){0,3}")
RUN_ID=re.compile(r"[1-9][0-9]{0,19}")
CODE=re.compile(r"[1-9][0-9]{0,9}")
APPLE_STATES={
    "READY_FOR_DISTRIBUTION":"ready for distribution","READY_FOR_SALE":"ready for sale",
    "WAITING_FOR_REVIEW":"waiting for review","IN_REVIEW":"in review",
    "PENDING_DEVELOPER_RELEASE":"approved; developer release pending",
    "PENDING_APPLE_RELEASE":"Apple release pending","PREPARE_FOR_SUBMISSION":"draft",
    "PROCESSING_FOR_DISTRIBUTION":"processing for distribution","READY_FOR_REVIEW":"ready for review",
    "ACCEPTED":"accepted","REJECTED":"rejected","METADATA_REJECTED":"metadata rejected",
    "DEVELOPER_REJECTED":"developer rejected","INVALID_BINARY":"invalid binary",
    "WAITING_FOR_EXPORT_COMPLIANCE":"export compliance pending"
}
PLAY_STATES={
    "PUBLISHED":"published on track","DRAFT":"draft, not available",
    "IN_REVIEW":"in review","NOT_SENT_FOR_REVIEW":"not submitted",
    "APPROVED_NOT_PUBLISHED":"approved, not published","NOT_APPROVED":"not approved",
    "UNSPECIFIED":"state unavailable"
}
BETA_STATES={"READY_FOR_BETA_TESTING":"ready; distribution not confirmed",
             "PROCESSING":"processing","PROCESSING_EXCEPTION":"processing failed",
             "MISSING_EXPORT_COMPLIANCE":"export compliance pending",
             "IN_EXPORT_COMPLIANCE_REVIEW":"export compliance review",
             "READY_FOR_BETA_SUBMISSION":"ready for beta submission",
             "WAITING_FOR_BETA_REVIEW":"waiting for beta review","IN_BETA_REVIEW":"beta review",
             "BETA_REJECTED":"beta rejected","EXPIRED":"expired"}

# Last provider observations already recorded by the existing release workflows.
# These are dated, not represented as a current store check.
HISTORICAL={
  "pack-one":{
    "beta":"[1.4 (101135), in beta testing · Nov 19](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/44459578296)",
    "play_production":"[101224 submitted for review · Nov 26](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/45762020071); [public app owner-confirmed Nov 19](https://github.com/killjoy00/mtg-ev-analyzer/issues/575)",
    "play_internal":"[101224 draft · Nov 26](https://github.com/killjoy00/mtg-ev-analyzer/actions/runs/45762020071); active tester version not checked"
  },
  "ez-trivia":{"play_internal":"[1.0.0-alpha12 (code 12) published · Nov 22](https://github.com/killjoy00/EZTrivia/actions/runs/45053275761)"},
  "gold-rush":{"play_internal":"[1.5.1 (code 4) internal + closed testing · Sep 18](https://github.com/killjoy00/GoldRush/issues/53)",
               "play_production":"[No releases as of Sep 18](https://github.com/killjoy00/GoldRush/issues/53); fresh check needed"},
  "star-run":{"play_internal":"[Code 2 completed; code 14 draft · Nov 25](https://github.com/killjoy00/EZTrivia/actions/runs/45716283565)",
              "beta":"[1.4 uploaded · Nov 25](https://github.com/killjoy00/EZTrivia/actions/runs/45715832907); tester availability not confirmed"}
}

def valid(pattern,value):
    return isinstance(value,str) and pattern.fullmatch(value) is not None


PACKONE_STATUS_ISSUE=1867
PACKONE_ISSUE_URL="https://api.github.com/repos/killjoy00/mtg-ev-analyzer/issues/1867"
ISSUE_MARKER=re.compile(r"<!-- portfolio-status:start -->\n"+r"\x60{3}json\n(.*?)\n\x60{3}\n<!-- portfolio-status:end -->",re.S)

def issue_snapshots(issue):
    if not isinstance(issue,dict) or issue.get("number")!=PACKONE_STATUS_ISSUE or "pull_request" in issue:
        return None,None
    body=issue.get("body")
    if not isinstance(body,str):
        return None,None
    matches=ISSUE_MARKER.findall(body)
    if len(matches)!=1:
        return None,None
    try:
        doc=json.loads(matches[0])
    except (ValueError,TypeError):
        return None,None
    if not isinstance(doc,dict) or not set(doc)<={"apple","play"}:
        return None,None
    return doc.get("apple"),doc.get("play")

def snapshots(repo,fetch):
    if repo=="killjoy00/mtg-ev-analyzer":
        return issue_snapshots(fetch(PACKONE_ISSUE_URL))
    if repo in TRUSTED_PUBLISHERS:
        return tuple(fetch(snapshot_url(repo,p)) for p in ("apple","play"))
    return None,None

def source(doc,app,field,identity,repo="killjoy00/EZTrivia",now=None):
    if repo not in TRUSTED_PUBLISHERS:
        return None,None
    if not isinstance(doc,dict) or doc.get("schema_version")!=1 or not valid(STAMP,doc.get("checked_at")) or not valid(RUN_ID,str(doc.get("run_id",""))):
        return None,None
    apps=doc.get("apps")
    row=apps.get(app) if isinstance(apps,dict) else None
    if not isinstance(row,dict) or not identity or row.get(field)!=identity:
        return None,None
    try:
        checked=dt.datetime.strptime(doc["checked_at"],"%Y-%m-%dT%H:%M:%SZ")
        current=dt.datetime.strptime(now,"%Y-%m-%d %H:%M") if now else checked
    except ValueError:
        return None,None
    if checked-current>dt.timedelta(minutes=10):
        return None,None
    label=checked.strftime("%Y-%m-%d %H:%M UTC")
    if current-checked>dt.timedelta(hours=36):
        label+=" · stale"
    return row,f" [{label}](https://github.com/{repo}/actions/runs/{doc['run_id']})"

def apple(doc,app,identity,repo="killjoy00/EZTrivia",now=None):
    row,stamp=source(doc,app,"bundle",identity,repo,now)
    if row is None:
        return None,None,None
    if row.get("result") not in ("ok","partial"):
        label="App record not returned" if row.get("result")=="not_found" else "Apple check unavailable"
        return label+stamp,label+stamp,label+stamp
    builds=row.get("builds",[])
    builds=[b for b in builds if isinstance(b,dict) and valid(VERSION,b.get("version")) and valid(VERSION,b.get("build"))] if isinstance(builds,list) else []
    active=next((b for b in builds if b.get("processing")=="VALID" and b.get("expired") is False and
                 (b.get("internal")=="IN_BETA_TESTING" or b.get("external")=="IN_BETA_TESTING")),None)
    beta=None
    if active:
        beta=f"{active['version']} ({active['build']}) in beta testing"+stamp
    newest=builds[0] if builds else None
    if newest and newest is not active:
        state=newest.get("processing")
        detail=BETA_STATES.get(newest.get("internal"),"uploaded; testing not confirmed") if state=="VALID" else ("processing" if state=="PROCESSING" else "invalid/failed" if state in ("INVALID","FAILED") else "processing unverified")
        newer=f"{newest['version']} ({newest['build']}) {detail}"+stamp
        beta=beta+"; newer: "+newer if beta else newer
    if not beta and row.get("result")=="ok" and not row.get("builds"):
        beta="No recent iOS build returned"+stamp
    versions=row.get("versions",[])
    versions=[v for v in versions if isinstance(v,dict) and valid(VERSION,v.get("version")) and v.get("state") in APPLE_STATES] if isinstance(versions,list) else []
    versions.sort(key=lambda v:tuple(int(x) for x in v["version"].split(".")),reverse=True)
    live=next((v for v in versions if v["state"] in ("READY_FOR_DISTRIBUTION","READY_FOR_SALE")),None)
    review=next((v for v in versions if v["state"] not in ("READY_FOR_DISTRIBUTION","READY_FOR_SALE")),None)
    published=f"{live['version']} {APPLE_STATES[live['state']]} (ASC)"+stamp if live else ("No ready-for-distribution version returned"+stamp if row.get("result")=="ok" and isinstance(row.get("versions"),list) else None)
    pending=f"{review['version']} {APPLE_STATES[review['state']]}"+stamp if review else ("No pending version returned"+stamp if row.get("result")=="ok" else None)
    return published,beta,pending

def play(doc,app,identity,track,repo="killjoy00/EZTrivia",now=None):
    row,stamp=source(doc,app,"package",identity,repo,now)
    if row is None:
        return None
    tracks=row.get("tracks")
    result=tracks.get(track) if isinstance(tracks,dict) else None
    if not isinstance(result,dict):
        return None
    if result.get("result")=="unavailable":
        return "Track check unavailable"+stamp
    if result.get("result")!="ok" or not isinstance(result.get("releases"),list):
        return None
    output=[]
    for rel in result["releases"]:
        if not isinstance(rel,dict) or rel.get("state") not in PLAY_STATES or not isinstance(rel.get("codes"),list):
            continue
        codes=[c for c in rel["codes"] if valid(CODE,c)]
        if codes:
            output.append("Code "+", ".join(codes)+" "+PLAY_STATES[rel["state"]])
        else:
            output.append(PLAY_STATES[rel["state"]]+" (code unavailable)")
    if not output:
        return "No active releases returned"+stamp if not result["releases"] else None
    return "; ".join(output)+stamp

def cells(app,apple_doc,play_doc,public,now=None):
    aid=app["id"]
    old=HISTORICAL.get(aid,{})
    ios,android=app["ios"],app["android"]
    repo=app.get("status_repo","killjoy00/EZTrivia")
    asc,beta,review=apple(apple_doc,aid,ios.get("bundle"),repo,now)
    ios_tracked=bool(ios.get("bundle") or ios.get("workflow"))
    play_tracked=bool(android.get("package") or android.get("workflow"))
    ia=("Awaiting store check" if app.get("status_repo") else "Store verification not configured") if ios_tracked else "Not tracked"
    ga=("Awaiting store check" if app.get("status_repo") else "Store verification not configured") if play_tracked else "Not tracked"
    public=public if public not in ("Not verified","Identity not verified") else (asc or ia)
    production=play(play_doc,aid,android.get("package"),"production",repo,now)
    # Owner confirmed Ministry is Android testing-only on 2026-11-26.
    # A later successful provider check always takes precedence.
    if aid=="ministry" and android.get("package")=="org.killjoy00.ministry" and (production is None or production.startswith("Track check unavailable")):
        production="Not live (owner confirmed Nov 26)"
    production=production or old.get("play_production") or ga
    internal=play(play_doc,aid,android.get("package"),"internal",repo,now) or old.get("play_internal") or ga
    return public,beta or old.get("beta") or ia,review or ia,production,internal
