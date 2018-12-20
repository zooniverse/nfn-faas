import os
import sys
import json
import urllib.parse as urlparse
from dateutil.parser import parse as dateparse
sys.path.append('/root/function')

from classification_parser import ClassificationParser

def handle(req):
    response = {}
    try:
        parsed_json = json.loads(req)
        parser = ClassificationParser(parsed_json)
    except (json.JSONDecodeError) as e:
        response = {'error': 'could not parse classification'}
        sys.exit(json.dumps(response))

    if 'workflow' in parser.params:
        response['workflow'] = parser.params['workflow']
    else:
        response['error'] = {'error': 'invalid workflow'}
        sys.exit(json.dumps(response))

    response['decade'] = check_decade(parser)
    response['country'] = parser.get_basic('country')
    response['state'] = parser.get_basic('state')
    response['time'] = check_time(parser)
    response['earth_day'] = earth_day(parser)

    print(json.dumps({k: v for k, v in response.items() if v is not None}))

def check_decade(parser):
    if 'year' in parser.params:
        year = parser.get_basic('year')
        if year:
            return "%s0s" % str(year)[-2]
        else:
            return None
    else:
        return None

def check_time(parser):
    if hasattr(parser, 'created_at'):
        time = dateparse(parser.created_at)
        if 3 <= time.hour < 9:
            return "earlybird"
        elif 9 <= time.hour < 15:
            return "lunchbreak"
        elif 15 <= time.hour < 21:
            return "dinnertime"
        else:
            return "nightowl"
    else:
        return None


def earth_day(parser):
    date = dateparse(parser.created_at)
    if date.day == 22 and date.month == 4:
        return True
    else:
        return None

