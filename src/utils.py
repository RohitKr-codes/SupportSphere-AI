import uuid
import re


def create_session_id():

    return str(
        uuid.uuid4()
    )


def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def confidence_to_percent(
    score
):

    return round(
        score * 100,
        2
    )


def truncate_text(
    text,
    length=200
):

    if len(text) <= length:
        return text

    return (
        text[:length] + "..."
    )