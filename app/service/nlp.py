import spacy

nlp = spacy.load("en_core_web_sm")

def process_text(command: str) -> str:
    doc = nlp(command)
    return doc.text.lower()  # Basic processing, can be improved
