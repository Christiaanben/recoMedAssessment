from datetime import datetime

import flask


def is_valid_iso8601(date_string):
    try:
        datetime.fromisoformat(date_string)
    except ValueError as e:
        flask.current_app.logger.error(e)
        return False
    return True
