import json
import sys
import requests.exceptions
from src.get_groups import get_groups
from src.parse_cmd_args import parse_cmd_args

# Set output encoding
sys.stdout.reconfigure(encoding='utf-8')

args = parse_cmd_args()

try:
    result = get_groups(args['faculty-id'], args['course'], args['structureId'])

except requests.exceptions.ConnectionError:
    sys.exit(json.dumps(
        {
            'success': False,
            'error_code': 0
        },
        indent=4,
        ensure_ascii=False
    ))

else:
    print(json.dumps(result, indent=4, ensure_ascii=False))
