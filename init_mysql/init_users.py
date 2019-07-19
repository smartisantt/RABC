import json
import logging

from django.db import transaction

from common.models import *
from rabc.settings import BASE_DIR


logger = logging.getLogger(__name__)

def main():
    json_file = BASE_DIR + "/init_mysql/users.json"
    with open(json_file, encoding="utf-8") as f:
        json_str = f.read()
        json_data = json.loads(json_str)

        try:
            with transaction.atomic():
                for item in json_data:
                    item['uuid'] = get_uuid()
                    User.objects.create(**item)

        except Exception as e:
            logging.error(str(e))





if __name__ == '__main__':
    main()