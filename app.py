from flask import Flask, jsonify, request

from helpers.date_helper import calculate_business_seconds, parse_iso8601, is_valid_iso8601
from enums.error_enums import INVALID_PARAMS

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
    calculated_business_seconds = calculate_business_seconds(start_time, end_time)
    return jsonify(calculated_business_seconds)
