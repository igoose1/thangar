import os
import sys

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
service_id = 777000

if api_id is None or api_hash is None:
    sys.exit("Provide $API_ID and $API_HASH.")
