import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]
AIRTABLE_API = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
ENC_KEY = os.environ["ENC_KEY"]

