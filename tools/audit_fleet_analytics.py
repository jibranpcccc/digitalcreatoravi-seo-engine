import os

expected_ids = {
    "site-1": "G-LAS1026001",
    "site-2": "G-WKR2026002",
    "site-3": "G-OAS3026003",
    "site-4": "G-ISA4026004",
    "site-5": "G-VEC5026005",
    "site-6": "G-NMD6026006",
    "site-7": "G-WHK7026007",
    "site-8": "G-DOC8026008",
    "site-9": "G-FRW9026009",
    "site-10": "G-RAG1026010",
    "site-11": "G-NPI1126011",
    "site-12": "G-SUM1226012",
    "site-13": "G-GLT1326013",
    "site-14": "G-SOC1426014",
    "site-15": "G-EOR1526015",
    "site-16": "G-DCH1626016",
    "site-17": "G-CRM1726017",
    "site-18": "G-CIP1826018",
    "site-19": "G-GKV1926019",
    "site-20": "G-ERH2026020",
}

print("=== FLEET-WIDE GOOGLE ANALYTICS & WEBMASTER VERIFICATION ===")
all_pass = True
for sid in sorted(expected_ids.keys(), key=lambda x: int(x.split("-")[1])):
    gid = expected_ids[sid]
    dist_path = os.path.join("sites", sid, "dist", "index.html")
    gsc_file = os.path.join("sites", sid, "public", "google6fe267a998c19a9a.html")
    
    if not os.path.exists(dist_path):
        print(f"FAIL: {sid} dist/index.html MISSING")
        all_pass = False
        continue
        
    html = open(dist_path, encoding="utf-8", errors="ignore").read()
    has_gtm = "googletagmanager.com/gtag/js?id=" in html
    has_id = gid in html
    has_gsc = "google6fe267a998c19a9a" in html
    has_bing = "BING-VERIFICATION" in html
    has_beacon = "webhookwatch.vercel.app/api/track" in html
    has_gsc_file = os.path.exists(gsc_file)
    
    passed = has_gtm and has_id and has_gsc and has_bing and has_beacon and has_gsc_file
    if not passed:
        all_pass = False
    
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {sid.ljust(8)} | GA: {gid} | GTM: {has_gtm} | ID: {has_id} | GSC Meta: {has_gsc} | GSC File: {has_gsc_file} | Bing: {has_bing} | Beacon: {has_beacon}")

print("=============================================================")
print(f"OVERALL STATUS: {'100% VERIFIED ACROSS ALL 20 SITES' if all_pass else 'VERIFICATION FAILED'}")
