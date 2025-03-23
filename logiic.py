import re
import spacy
from dateutil.parser import parse
from datetime import datetime

#JK Ka project Final Logic

try:
    nlp = spacy.load("en_core_web_lg") 
except Exception as e:
    print(f"⚠ Error loading NLP model: {e}")
    nlp = None

def extract_event_details(text):
    if not nlp:
        return {"summary": "Error", "description": "NLP Model not loaded", "start_date": None, 
                "end_date": None, "start_time": None, "end_time": None, "location": None}

    doc = nlp(text)

    extracted_data = {
        "summary": None,
        "description": None,
        "start_date": None,
        "end_date": None,
        "start_time": None,
        "end_time": None,
        "location": None
    }

    dates, times, locations = [], [], []
    sentences = list(doc.sents)  

    time_pattern = re.compile(r'\b(?:[01]?\d|2[0-3]):?[0-5]\d\s?(?:AM|PM|am|pm)?\b')
    for ent in doc.ents:
        if ent.label_ == "DATE":
            try:
                parsed_date = parse(ent.text, fuzzy=True).strftime("%Y-%m-%d")
                dates.append(parsed_date)
            except:
                continue
        elif ent.label_ == "TIME":
            times.append(ent.text)
        elif ent.label_ in ["GPE", "LOC", "FAC"]:
            locations.a
    times.extend(time_pattern.findall(text))

    extracted_data["start_date"] = dates[0] if dates else None
    extracted_data["end_date"] = dates[-1] if len(dates) > 1 else extracted_data["start_date"]

    if extracted_data["start_time"] is None:
        extracted_data["start_time"] = "00:00"
    if extracted_data["end_time"] is None:
        extracted_data["end_time"] = extracted_data["start_time"] 

    extracted_data["location"] = locations[0] if locations else None

    if sentences:
        extracted_data["summary"] = sentences[0].text.strip()
        extracted_data["description"] = " ".join([s.text.strip() for s in sentences[1:]])

    return extracted_data
