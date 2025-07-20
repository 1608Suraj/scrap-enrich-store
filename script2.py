import json
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "DataBase_Name"
RAW_JSON_PATH = "Output_FileName.json"
FILTERED_COLLECTION = "Collection_Name"

def try_parse_float(value):
    try:
        return float(str(value).replace(",", "").replace("$", "").strip())
    except:
        return None

def extract_country(loc):
    if not loc:
        return None

    if isinstance(loc, str):
        loc = [loc]

    for entry in loc:
        if not isinstance(entry, str):
            continue
        parts = entry.split(",")
        if parts:
            country = parts[-1].strip().lower()
            if len(country) == 2:
                return country.upper()
            if "usa" in country or "united states" in country:
                return "US"
            if "uk" in country or "united kingdom" in country:
                return "UK"
            
            return country.title()  
    return None  


def main():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[FILTERED_COLLECTION]

    # Drop old filtered collection
    collection.drop()
    print(f"🗑️  Dropped old '{FILTERED_COLLECTION}' collection.")

    # Load raw JSON data
    with open(RAW_JSON_PATH, encoding="latin-1") as f:
        logistics = json.load(f)

    # Filter and prepare data
    ops = []
    for doc in logistics:
        name = doc.get("name")
        if not name:
            continue

        all_locations = doc.get("all_locations")
        if isinstance(all_locations, str):
            locations_list = [all_locations]
        elif isinstance(all_locations, list):
            locations_list = all_locations
        else:
            locations_list = []

        # Safely get domain from industries (last element if list, else None)
        industries = doc.get("industries")
        if isinstance(industries, list) and industries:
            domain = industries[-1]
        elif isinstance(industries, str):
            domain = industries
        else:
            domain = None

        # Safely get year from batch (last word if string, else None)
        batch = doc.get("batch")
        if isinstance(batch, str) and batch.strip():
            year = batch.strip().split(" ")[-1]
        else:
            year = None

        filtered_doc = {
            "country": extract_country(locations_list),
            "source_url": doc.get("url"),
            "name": name,
            "domain": domain,
            "website": doc.get("website"),
           "arr": try_parse_float(doc.get("ARR")),
            "year": year,
            "team_size": doc.get("team_size"),
            "headquarter": all_locations,
            "no_of_locations": doc.get("no_of_location"),
            "growthRate": doc.get("growthRate")
        }

        ops.append(UpdateOne(
            {"name": filtered_doc["name"]},  # Unique identifier
            {"$set": filtered_doc},
            upsert=True
        ))

    if ops:
        collection.bulk_write(ops)
        print(f"✅ Uploaded {len(ops)} filtered records to '{FILTERED_COLLECTION}'.")

if __name__ == "__main__":
    main()