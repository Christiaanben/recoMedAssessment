from datetime import datetime

import flask


def is_valid_iso8601(date_string) -> bool:
    try:
        datetime.fromisoformat(date_string)
    except ValueError as e:
        flask.current_app.logger.error(e)
        return False
    return True


def parse_iso8601(date_string):
    return datetime.fromisoformat(date_string)

