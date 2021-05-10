import json
from solve import solve

def handle(event, context):
    event = json.loads(event['body']) if 'body' in event else {}
    if event and 'people' in event and 'settings' in event and 'shifts' in event:
        result = json.dumps(solve(event['people'], event['settings'], event['shifts']))
    else:
        result = '{"bad": ' + json.dumps(event) + '}'

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': result
    }