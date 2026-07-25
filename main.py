from docx import Document
import sys

from image_redactor import redact_images
from replace_images import replace_images
from extract_images import extract_images
from reader import extract_text
from detector import detect_pii, detect_entities
from replacer import (
    replace_emails,
    replace_phones,
    replace_persons,
    replace_ssn,
    replace_credit_cards,
    replace_ip,
    replace_dob,
    apply_replacements
)

# Enable UTF-8 output for ruppees sign and stuff
sys.stdout.reconfigure(encoding="utf-8")


def clean_persons(persons):

    INVALID_PERSONS = {
        "Offer", "Issue", "Date", "Email", "Telephone",
        "Website", "Bid", "Promoter", "Promoters",
        "Registrar", "Share", "Shares", "Board",
        "Company", "Offer Price", "Floor Price",
        "Cap Price", "Mutual Funds"
    }

    cleaned = []

    for person in persons:

        if person in INVALID_PERSONS:
            continue

        if len(person.split()) < 2:
            continue

        if person.isdigit():
            continue

        cleaned.append(person)

    return list(set(cleaned))


def process_document(input_path, output_path):
    print("Extracting images...")
    extract_images(input_path)

    print("Redacting sensitive images...")
    redact_images()

    temp_doc = "output/redacted_with_images.docx"

    print("Replacing images inside document...")
    replace_images(
    input_path,
    temp_doc
)

    doc = Document(temp_doc)
    text = extract_text(doc)

    print("=" * 60)
    print("DOCUMENT LOADED SUCCESSFULLY")
    print("=" * 60)

    print("\nFirst 1000 characters:\n")
    print(text[:1000])
    pii = detect_pii(text)
    entities = detect_entities(text)
    entities["PERSON"] = clean_persons(entities["PERSON"])

    print("\n\nTEXT PII")
    print("=" * 60)

    for category, values in pii.items():

        print(f"\n{category}")
        print("-" * 40)

        if not values:
            print("No matches found.")
        else:
            for value in values:
                print(value)
    print("\n\nNAMED ENTITIES")
    print("=" * 60)

    for category, values in entities.items():

        print(f"\n{category}")
        print("-" * 40)

        if not values:
            print("No matches found.")
        else:
            for value in values:
                print(value)
    email_map = replace_emails(pii["EMAIL"])
    phone_map = replace_phones(pii["PHONE"])
    person_map = replace_persons(entities["PERSON"])
    
    ssn_map = replace_ssn(pii["SSN"])
    credit_map = replace_credit_cards(pii["CREDIT_CARD"])
    ip_map = replace_ip(pii["IP"])
    dob_map = replace_dob(pii["DOB"])

    replacement_map = {}

    replacement_map.update(email_map)
    replacement_map.update(phone_map)
    replacement_map.update(person_map)
    replacement_map.update(ssn_map)
    replacement_map.update(credit_map)
    replacement_map.update(ip_map)
    replacement_map.update(dob_map)

    print("\nTotal replacements :", len(replacement_map))

    print("\nEMAIL REPLACEMENTS")
    print("=" * 60)
    for old, new in email_map.items():
        print(f"{old} ---> {new}")

    print("\nPHONE REPLACEMENTS")
    print("=" * 60)
    for old, new in phone_map.items():
        print(f"{old} ---> {new}")

    print("\nPERSON REPLACEMENTS")
    print("=" * 60)
    for old, new in person_map.items():
        print(f"{old} ---> {new}")

    print("\nSSN REPLACEMENTS")
    print("=" * 60)
    for old, new in ssn_map.items():
        print(f"{old} ---> {new}")

    print("\nCREDIT CARD REPLACEMENTS")
    print("=" * 60)
    for old, new in credit_map.items():
        print(f"{old} ---> {new}")

    print("\nIP ADDRESS REPLACEMENTS")
    print("=" * 60)
    for old, new in ip_map.items():
        print(f"{old} ---> {new}")

    print("\nDOB REPLACEMENTS")
    print("=" * 60)
    for old, new in dob_map.items():
        print(f"{old} ---> {new}")

    doc = apply_replacements(doc, replacement_map)

    doc.save(output_path)

    print("\n")
    print("=" * 60)
    print("FINAL REDACTED DOCUMENT CREATED")
    print(f"Location : {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    process_document(
        "input/ticket.docx",
        "output/redacted.docx"
    )