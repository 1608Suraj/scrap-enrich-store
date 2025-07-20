import json
import time
from datetime import datetime
import groq
from dotenv import load_dotenv
import os

# === CONFIG === #
OUTPUT_JSON_PATH = "OutPut_FileName.json"
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
RAW_JSON_PATH = "fileName.json"

def try_parse_float(value):
    try:
        return float(str(value).replace(",", "").replace("$", "").strip())
    except:
        return None


def enrich_with_groq(name):
    client = groq.Groq(api_key=GROQ_API_KEY)

    prompt = (
        f"Estimate the ARR (Annual Recurring Revenue in USD, number only) and growth rate (high, medium, low), and the number of locations (number only) "
        f"for the tech logistics company '{name}'. Respond ONLY in raw JSON like this:\n"
        f'{{"ARR": 20.0, "growthRate": "low", "no_of_location": 1}}\n\n'
        f"Use null for unknown values. DO NOT return explanations or text outside the JSON."
        f"Make sure Not to use assumtion for ARR and growthRate Should be depend on the company Arr and no of employes they have according to current market Depend on there valuation."

    )

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        return {
            "ARR": try_parse_float(parsed.get("ARR")),
            "growthRate": parsed.get("growthRate"),
            "no_of_location": parsed.get("no_of_location")
        }
    except Exception as e:
        print(f"❌ Error enriching '{name}': {e}")
        return {"ARR": None, "growthRate": None, "no_of_location": 1}


def main(RAW_JSON_PATH):

    with open(RAW_JSON_PATH, encoding="latin-1") as f:
        logistics_data = json.load(f)
    enriched_data = []

    for idx, doc in enumerate(logistics_data):
        name = doc.get("name")
        if not name:
            continue

        existing_arr = try_parse_float(doc.get("ARR"))
        existing_growth = doc.get("growthRate")
        existing_no_of_loc = doc.get("no_of_location")


        # Enrich if missing
        if existing_arr is None or not isinstance(existing_growth, str) or existing_no_of_loc is None:
            enriched = enrich_with_groq(name)
            if existing_arr is None:
                doc["ARR"] = enriched["ARR"]
            if not isinstance(existing_growth, str):
                doc["growthRate"] = enriched["growthRate"]
            if existing_no_of_loc is None:
                doc["no_of_location"] = enriched["no_of_location"]
            time.sleep(0)  # To respect rate limits

        enriched_data.append(doc)

    # Save to new JSON file
    with open(OUTPUT_JSON_PATH, "w", encoding="latin-1") as out_f:
        json.dump(enriched_data, out_f, indent=2)

    print(f"\n✅ Enrichment complete! Output saved to '{OUTPUT_JSON_PATH}'")


if __name__ == "__main__":
    main()