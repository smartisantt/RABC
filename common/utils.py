import re
import uuid


NICKNAME_PATTERN = re.compile(r'^\w{3,20}$')
TEL_PATTERN = re.compile(r'^1[3-9]\d{9}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$')


def get_uuid():
    return "".join(str(uuid.uuid4()).split("-")).upper()