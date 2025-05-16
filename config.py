import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

QUESTS_DIR = "quests"
PROFILES_DIR = "profiles"

RELATIONSHIP_LEVELS = {
    0: "незнакомец",
    1: "друг",
    2: "близкий друг",
    3: "романтические отношения",
    4: "возлюбленная"
}
