"""
Content Decay Detector & Striking-Distance Query Identifier (Positions 4-20)
"""
def detect_decay_and_opportunities(gsc_rows):
    opportunities = {
        "striking_distance": [],
        "decaying": [],
        "low_ctr": [],
        "cannibalization": []
    }

    for row in gsc_rows:
        pos = row.get("position", 50)
        impressions = row.get("impressions", 0)
        ctr = row.get("ctr", 0.0)

        # Striking Distance: Positions 4 to 20
        if 4.0 <= pos <= 20.0 and impressions > 100:
            opportunities["striking_distance"].append(row)

        # Low CTR: Many impressions, CTR < 2%
        if impressions > 500 and ctr < 0.02 and pos < 10:
            opportunities["low_ctr"].append(row)

    return opportunities
