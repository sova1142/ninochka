import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv(8084573722:AAGSWWej0tSfH6-eBvQDG-W444tM2AQ0KqA)
QWEN_API_KEY = os.getenv(eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwZDg3YjhlLWFkNTgtNDBmZS05YWQ2LTQ5MTk2MDI1MDFmZiIsImV4cCI6MTc0OTc5NjMyNn0.CZgXzy2cQLfDczanuQ9p6TZBSRu1VdEF7V2XLpn2t84)

QUESTS_DIR = "quests"
PROFILES_DIR = "profiles"

RELATIONSHIP_LEVELS = {
    0: "незнакомец",
    1: "друг",
    2: "близкий друг",
    3: "романтические отношения",
    4: "возлюбленная"
}
