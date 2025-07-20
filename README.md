
# 🚀 Data Scrap-Enrich-Store

This project automates the complete pipeline of:

1. **Scraping company data** from a public API.
2. **Enriching missing fields** like ARR (Annual Recurring Revenue), growth rate, and number of locations using the **Groq LLM API**.
3. **Filtering and cleaning** the dataset.
4. **Uploading enriched records** into a **MongoDB** database.

> ✅ You can **modify this project** to apply custom filters or enrich additional fields based on your specific needs.

---

## 📂 Project Structure

```
Scrap-enrich-store/
├── script.py             # Step 1: Scrape company data from a public API
├── script1.py            # Step 2: Enrich missing values using Groq LLM
├── script2.py            # Step 3: Filter, format, and upload to MongoDB
├── logistics.json        # Raw scraped data (output from script.py)
├── enriched_logistics4.json # Enriched data (output from script1.py)
```
<p align="center">
  <img src="https://raw.githubusercontent.com/1608Suraj/scrap-enrich-store/main/diagram.png" width="600"/>
</p>

---

## 🧠 Features

- 🔁 End-to-end automation of data pipeline
- 🔍 Smart field enrichment with Groq
- 🔧 Easy-to-modify filtering and transformation logic
- ☁️ Uploads to local or cloud-hosted MongoDB
- 📦 Lightweight and dependency-minimal

---

## 🔧 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/1608Suraj/scrap-enrich-store.git
   cd scrap-enrich-store
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys:
   - Add your **Public Sources API key** in `script.py`
   - Add your **Groq API key** in `script1.py`
   - Set your **MongoDB URI** in `script2.py`

---

## ⚙️ Configuration

### MongoDB (in `script2.py`)
```python
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "logistics"
FILTERED_COLLECTION = "auto"
```

### Groq API Key (in `script1.py`)
```python
GROQ_API_KEY = "your_groq_api_key"
```

---

## 🚀 Pipeline Usage

### Step 1: Fetch Raw Company Data
```bash
python script.py
```
This saves the raw dataset to `logistics.json`.

### Step 2: Enrich Using Groq
```bash
python script1.py
```
This enriches missing `ARR`, `growthRate`, and `no_of_location` and saves the results to `enriched_logistics4.json`.

### Step 3: Filter and Upload to MongoDB
```bash
python script2.py
```

---

## 🧩 Customize Your Filters

- Want to **filter by ARR, growthRate, year, domain**, etc.? Modify the logic in `script2.py` under `filtered_doc`.
- Want to **enrich more fields** using Groq? Change the prompt in `script1.py`.
- Want to add error logs, retry mechanisms, or a CLI? Easily extend the modular scripts.

---

## 🧪 Country Extraction Logic

```python
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
```

---

## ✅ MongoDB Output Format

A sample document stored in MongoDB:

```json
{
  "name": "Example Logistics Co",
  "country": "Germany",
  "domain": "Supply Chain",
  "website": "https://example.com",
  "arr": 25.0,
  "growthRate": "medium",
  "no_of_locations": 3,
  "year": "2020",
  "team_size": "50-100",
  "headquarter": ["Berlin, Germany"],
  "source_url": "https://example-source.com"
}
```

---

## 💡 Additional From Your Side

- [ ] Add automatic logging and error handling
- [ ] Connect to Groq via async for faster enrichment
- [ ] Create a Streamlit dashboard for visualizing data
- [ ] Integrate with additional APIs for enrichment

---

## 📄 License

MIT License

---

## 🙌 Contributions

Feel free to fork, improve, and submit a pull request. Contributions are always welcome!
