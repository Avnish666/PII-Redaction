import re
import spacy

nlp = spacy.load("en_core_web_sm")

INVALID_ENTITIES = {
    "Offer", "Issue", "Price", "Share", "Shares",
    "Promoter", "Promoters", "Board", "Committee",
    "Registrar", "Telephone", "Email", "Website",
    "Date", "Period", "Floor Price", "Cap Price",
    "Mutual Funds", "Regulation", "Prospectus",
    "Book", "Running", "Lead", "Manager",
    "Stock Exchange", "Financial", "General",
    "Risk", "Section"
}

PERSON_BLACKLIST = {
    "Road", "Lane", "Street",
    "Offer", "Issue", "Price", "Share", "Shares",
    "Capital", "Regulation", "Committee", "Board",
    "Telephone", "Email", "Website",
    "Acknowledgement", "Slip", "Transfer",
    "Application", "Investor", "Registrar",
    "Promoter", "Promoters", "Bid", "Form",
    "Book", "Running", "Lead", "Manager",
    "Managers", "Mutual", "Fund", "Funds"
}



EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

MOBILE_PATTERN = r"\b(?:\+91[-\s]?|91[-\s]?)?[6-9]\d{9}\b"

LANDLINE_PATTERN = r"\b(?:\+91[-\s]?)?(?:0?\d{2,4}[-\s]?)?\d{6,8}\b"

URL_PATTERN = r"\b(?:https?://|www\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?\b"

IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

SSN_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b"

CREDIT_CARD_PATTERN = r"\b(?:\d[ -]*?){13,16}\b"

DOB_PATTERN = r"\b(?:0?[1-9]|[12][0-9]|3[01])[/-](?:0?[1-9]|1[0-2])[/-](?:19|20)\d{2}\b"


def detect_pii(text):

    pii = {}

    pii["EMAIL"] = sorted(set(re.findall(EMAIL_PATTERN, text)))

    phones = set()
    phones.update(re.findall(MOBILE_PATTERN, text))
    phones.update(re.findall(LANDLINE_PATTERN, text))
    pii["PHONE"] = sorted(phones)

    pii["URL"] = sorted(set(re.findall(URL_PATTERN, text)))

    pii["IP"] = sorted(set(re.findall(IP_PATTERN, text)))

    pii["SSN"] = sorted(set(re.findall(SSN_PATTERN, text)))

    pii["DOB"] = sorted(set(re.findall(DOB_PATTERN, text)))

    pii["CREDIT_CARD"] = sorted(set(re.findall(CREDIT_CARD_PATTERN, text)))

    return pii


def detect_entities(text):

    doc = nlp(text)

    persons = set()
    organizations = set()
    locations = set()

    for ent in doc.ents:

        value = ent.text.strip()

        if len(value) < 3:
            continue

        if value.replace(" ", "").isdigit():
            continue

        if value in INVALID_ENTITIES:
            continue

      
        if ent.label_ == "PERSON":

            words = value.split()

            if not (2 <= len(words) <= 4):
                continue

            if any(ch.isdigit() for ch in value):
                continue

            if value.isupper():
                continue

            if any(word in PERSON_BLACKLIST for word in words):
                continue

            persons.add(value)



    return {
        "PERSON": sorted(persons)
    }