from flask import Flask, jsonify, request

from helpers.date_helper import parse_iso8601, next_business_time, calculate_business_time_for_today_after, \
    calculate_business_time_for_today_before, calculate_business_days_between
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
    business_start_time = next_business_time(start_time)
    if business_start_time.date() == end_time.date():
        time_diff = end_time - business_start_time
        return jsonify(int(time_diff.total_seconds()))
    business_seconds_on_start_date = calculate_business_time_for_today_after(start_time)
    business_seconds_on_end_date = calculate_business_time_for_today_before(end_time)
    business_days_between_dates = calculate_business_days_between(business_start_time, end_time)
    return jsonify(business_seconds_on_start_date + business_days_between_dates * 9 * 60 * 60 + business_seconds_on_end_date)

