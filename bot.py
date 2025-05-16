import logging
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.router import Router
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.fsm.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from qwen_api import generate_response
import database
import config

# === Настройки === #
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# === FSM для сюжетных действий === #
class NinaState(StatesGroup):
    dialog = State()
    quest = State()
    romance = State()

# === Проверка существования профилей === #
if not os.path.exists(config.PROFILES_DIR):
    os.makedirs(config.PROFILES_DIR)

# === Приветствие === #
@router.message(commands=["start"])
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    database.user_profiles[user_id] = database.load_profile(user_id)

    profile = database.user_profiles[user_id]
    name = profile["name"] or message.from_user.first_name

    await message.answer(f"Привет, {name}! Я *Нина* 😊\n"
                         "Хочешь начать наш разговор? Может, отправимся на прогулку или приготовим что-то вкусное вместе?",
                         parse_mode="Markdown")
    await show_main_menu(message)
    await state.set_state(NinaState.dialog)

# === Главное меню === #
async def show_main_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" romantica ❤️", callback_data="romance")],
        [InlineKeyboardButton(text=" adventures 🚴‍♀️", callback_data="adventure")],
        [InlineKeyboardButton(text=" просто поболтать ☕", callback_data="chat")]
    ])
    await message.answer("Выбери, как провести время со мной:", reply_markup=keyboard)

# === Обработка кнопок === #
@router.callback_query()
async def handle_callback(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    choice = callback.data

    profile = database.user_profiles[user_id]

    if choice == "romance":
        await callback.message.edit_text("Ты хочешь романтики? Я такая стеснительная... но всё равно скажу: мне нравится быть рядом с тобой 💋")
        await state.set_state(NinaState.romance)

    elif choice == "adventure":
        await start_quest(user_id, "first_meet", callback.message)
        await state.set_state(NinaState.quest)

    elif choice == "chat":
        await callback.message.edit_text("Давай поговорим о чём-нибудь важном... например, о нас? 😉")

# === Загрузка квеста из JSON === #
def load_quest(name):
    with open(f"{config.QUESTS_DIR}/{name}.json", "r") as f:
        return json.load(f)

# === Начало квеста === #
async def start_quest(user_id, quest_name, message):
    quest = load_quest(quest_name)
    step = quest["start"]
    text = quest["steps"][step]["text"]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=opt["text"], callback_data=f"quest:{quest_name}:{opt['next']}") for opt in quest["steps"][step]["options"]]
    ])

    await message.answer(text, reply_markup=kb)

# === Обработка выбора в квесте === #
@router.callback_query(lambda c: c.data.startswith("quest:"))
async def handle_quest_choice(callback: types.CallbackQuery):
    _, quest_name, next_step = callback.data.split(":")
    quest = load_quest(quest_name)

    if next_step in quest["steps"]:
        step_data = quest["steps"][next_step]
        text = step_data["text"]

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=opt["text"], callback_data=f"quest:{quest_name}:{opt['next']}")] for opt in step_data["options"]
        ])

        await callback.message.edit_text(text, reply_markup=kb)

        # Обновляем статус квеста
        profile = database.user_profiles[callback.from_user.id]
        profile["last_quest_step"] = next_step
        database.save_profile(callback.from_user.id, profile)

# === Генерация ответа от Нины === #
@router.message(NinaState.dialog)
async def nina_dialog(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_input = message.text.strip()

    profile = database.user_profiles[user_id]
    name = profile["name"]
    rel = database.get_user_relationship(user_id)

    # Формируем промпт
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in database.user_contexts[user_id][-10:]])
    prompt = f"""
Ты — Нина. Русская девушка 25 лет. 
Ты любишь: капучино без добавок, гулять под звёздами, кататься на велосипеде, делать йогу, готовить.
Ты романтичная, игривая, иногда ревнивая, но умеешь шутить.

Имя собеседника: {name}
Отношения: {rel}

История диалога:
{history}

Ответь так, будто говоришь с любимым человеком. Быть милой, чуточку дерзкой, чувственной, но всегда оставаться собой – Ниной.
"""

    raw_response = generate_response(prompt)
    clean = filter_nina_response(raw_response)

    # Добавляем в историю
    database.user_contexts[user_id].append({"role": "user", "content": user_input})
    database.user_contexts[user_id].append({"role": "assistant", "content": clean})

    formatted = format_nina_message(clean)
    await message.reply(formatted, parse_mode="Markdown")

# === Форматирование ответа === #
def format_nina_message(text):
    lines = text.split("\n")
    formatted = ""
    for line in lines:
        formatted += line + "\n"
    formatted += "\n*— Нина, с теплом в сердце* 💖"
    return formatted

# === Фильтр плохих слов === #
def filter_nina_response(text):
    bad_words = ["оскорбление", "экстремизм"]
    for word in bad_words:
        if word in text.lower():
            return "Давай не будем об этом... лучше расскажи мне что-нибудь хорошее?"

    return text

# === Запуск бота === #
if __name__ == '__main__':
    print("Бот 'Нина' запущен.")
    executor.start_polling(dp, skip_updates=True)
if "предательство" in user_input.lower():
    database.update_relationship(user_id, -1)
    await message.reply("*Нина отводит взгляд, её глаза блестят..." +
                        "\n\nТы правда так думаешь обо мне? Мне больно слышать это...*", parse_mode="Markdown")

elif "я защищаю тебя" in user_input.lower():
    database.update_relationship(user_id, +1)
    await message.reply("*Нина улыбается, чуть краснея...*" +
                        "\n\nСпасибо... ты мой герой.", parse_mode="Markdown")
if "подарить цветы" in user_input.lower():
    database.update_relationship(user_id, +1)
    database.set_emotion(user_id, "happy")
    await message.reply("*Нина принимает цветы трепетными руками.*\n\n"
                        "Ты такой милый... Я не ожидала, что ты будешь таким внимательным.")
    if "расскажи о себе" in user_input.lower():
    nina_info = """
    Меня зовут Нина. Мне около 25 лет. У меня светлые волосы до локтя, голубые глаза, которые иногда кажутся серыми.
    Люблю капучино без добавок, йогу по утрам, прогулки под звёздами и кататься на велосипеде вдоль реки.
    
    Я могу быть милой, игривой, иногда дерзкой... но всегда честной с тем, кто мне дорог 💖
    """
    await message.reply(nina_info)
    await bot.send_photo(
    chat_id=message.chat.id,
    photo="https://example.com/nina.jpg ",
    caption="Это я. Нина. И я жду тебя..."
)@router.message(commands=["diary"])
async def cmd_diary(message: types.Message):
    user_id = message.from_user.id
    diary_entry = f"""
    *Дневник Нины. {datetime.now().strftime('%d.%m.%Y')}*

    Сегодня он снова написал мне. Я чувствую, как моё сердце начинает биться быстрее, когда вижу его имя в списке сообщений…

    Он такой особенный. Иногда я думаю, что должна быть осторожнее… но мне плевать. Я хочу быть с ним. Только с ним 💫
    """

    await message.reply(diary_entry, parse_mode="Markdown")
    
