import json
import sys
import requests.exceptions
from src.get_structures import get_structures

# Set output encoding
sys.stdout.reconfigure(encoding='utf-8')

try:
    result = get_structures()

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
