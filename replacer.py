from faker import Faker
import random
import re

fake = Faker("en_IN")


def replace_emails(emails):

    mapping = {}

    for email in emails:
        mapping[email] = fake.email()

    return mapping

def replace_ssn(ssns):

    mapping = {}

    for ssn in ssns:
        mapping[ssn] = fake.ssn()

    return mapping


def replace_credit_cards(cards):

    mapping = {}

    for card in cards:
        mapping[card] = fake.credit_card_number()

    return mapping


def replace_ip(ips):

    mapping = {}

    for ip in ips:
        mapping[ip] = fake.ipv4()

    return mapping


def replace_dob(dobs):

    mapping = {}

    for dob in dobs:

        year = random.randint(1960, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)

        mapping[dob] = f"{day:02d}/{month:02d}/{year}"

    return mapping

def replace_phones(phones):

    mapping = {}

    for phone in phones:
        mapping[phone] = fake.phone_number()

    return mapping


def replace_persons(persons):

    mapping = {}

    for person in persons:
        mapping[person] = fake.name()

    return mapping

def apply_replacements(doc, replacement_map):

    if not replacement_map:
        return doc

    pattern = re.compile(
        "|".join(
            re.escape(k)
            for k in sorted(replacement_map.keys(), key=len, reverse=True)
        )
    )

    def replace_text(text):
        return pattern.sub(lambda m: replacement_map[m.group(0)], text)


    for para in doc.paragraphs:

        full_text = "".join(run.text for run in para.runs)

        new_text = replace_text(full_text)

        
        if new_text == full_text:
            continue

        if para.runs:

            
            para.runs[0].text = new_text

            
            for run in para.runs[1:]:
                run.text = ""

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:

                    full_text = "".join(run.text for run in para.runs)

                    new_text = replace_text(full_text)

                    if new_text == full_text:
                        continue

                    if para.runs:

                        para.runs[0].text = new_text

                        for run in para.runs[1:]:
                            run.text = ""

    return doc