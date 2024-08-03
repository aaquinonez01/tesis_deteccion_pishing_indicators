import re
import email
from email import policy
from email.parser import BytesParser


def extract_email_data(email_content):
    msg = BytesParser(policy=policy.default).parsebytes(email_content.encode())

    # body = get_body(msg)

    urls, body_without_urls = extract_urls_and_clean_body(email_content)

    return {"body": body_without_urls, "urls": urls}


def get_body(msg):
    if msg.is_multipart():
        for part in msg.iter_parts():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        print(msg)
        return msg.get_payload(decode=True).decode(msg.get_content_charset())

    return ""


def extract_urls_and_clean_body(text):
    url_regex = re.compile(r"https?://\S+")
    urls = url_regex.findall(text)
    body_without_urls = url_regex.sub("", text)
    return urls, body_without_urls.strip()


email_content = """The academic discipline of Software Engineering was launched at a conference
sponsored by NATO, at Garmisch, Germany, in October, 1968. Intriguingly, the
term Software Engineering was chosen to be deliberately provocative -- why
can't software be developed with the same rigor used by other engineering
disciplines?The proceedings of this conference are now available online, at:
http://www.cs.ncl.ac.uk/old/people/brian.randell/home.formal/NATO/index.htmlAlso, don't miss the pictures of attendees, including many significant
contributors to the field of Software Engineering:
http://www.cs.ncl.ac.uk/old/people/brian.randell/home.formal/NATO/N1968/index.html- Jim"""
email_data = extract_email_data(email_content)
print(email_data)
