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
