from flask import Flask, jsonify, request

from helpers.date_helper import parse_iso8601
from .enums.error_enums import INVALID_PARAMS
from .helpers.date_helper import is_valid_iso8601

app = Flask(__name__)


@app.route('/')
def status():
    return 'Server online.'


@app.route('/api/business-seconds')
def business_seconds():
    start_time, end_time = request.args.get('start_time'), request.args.get('end_time')
    if not (is_valid_iso8601(start_time) and is_valid_iso8601(end_time)):
        return jsonify(dict(error=INVALID_PARAMS)), 400
    start_time, end_time = parse_iso8601(start_time), parse_iso8601(end_time)
    time_diff = end_time - start_time
    print(time_diff)
    print(type(time_diff))
    return jsonify(int(time_diff.total_seconds()))
