import os
import json
from collections import defaultdict

user_contexts = defaultdict(list)  # контекст диалога
user_profiles = {}  # данные пользователя

def load_profile(user_id):
    path = f"profiles/{user_id}.json"
    if not os.path.exists(path):
        return {
            "name": None,
            "relationship_level": 0,
            "preferences": {},
            "completed_quests": [],
            "last_quest_step": {}
        }
    with open(path, "r") as f:
        return json.load(f)

def save_profile(user_id, data):
    with open(f"profiles/{user_id}.json", "w") as f:
        json.dump(data, f, indent=4)

def get_user_relationship(user_id):
    profile = user_profiles.get(user_id)
    return config.RELATIONSHIP_LEVELS.get(profile["relationship_level"], "неизвестно")
def update_relationship(user_id, delta=1):
    profile = user_profiles[user_id]
    profile["relationship_level"] = max(0, min(4, profile["relationship_level"] + delta))
    save_profile(user_id, profile)
RELATIONSHIP_LEVELS = {
    0: "незнакомец",
    1: "друг",
    2: "близкий друг",
    3: "романтические отношения",
    4: "возлюбленная"
}

EMOTIONAL_STATES = {
    "neutral": {"emoji": "🙂", "description": "спокойна"},
    "happy": {"emoji": "🥰", "description": "в восторге от тебя"},
    "sad": {"emoji": "😢", "description": "грустна"},
    "angry": {"emoji": "😤", "description": "сердита"},
    "flirty": {"emoji": "💋", "description": "играю с тобой"},
    "jealous": {"emoji": "👀", "description": "ревную"}
}def update_relationship(user_id, delta=1):
    profile = user_profiles[user_id]
    profile["relationship_level"] = max(0, min(4, profile["relationship_level"] + delta))
    save_profile(user_id, profile)

def set_emotion(user_id, emotion):
    profile = user_profiles[user_id]
    profile["emotion"] = emotion
    save_profile(user_id, profile)
