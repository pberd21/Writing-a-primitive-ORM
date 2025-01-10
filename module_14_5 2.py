from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import crud_functions 

API_TOKEN = ""  
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"), KeyboardButton("Купить"), KeyboardButton("Регистрация"))

inline_keyboard = InlineKeyboardMarkup(row_width=1)
inline_keyboard.add(
    InlineKeyboardButton("Product1", callback_data="product_buying"),
    InlineKeyboardButton("Product2", callback_data="product_buying"),
    InlineKeyboardButton("Product3", callback_data="product_buying"),
    InlineKeyboardButton("Product4", callback_data="product_buying")
)

@dp.message_handler(commands=["start"])
async def start(message: Message):
    crud_functions.initiate_db()
    products = crud_functions.get_all_products()
    if products:
        await message.reply("Продукты в базе данных загружены!")
    else:
        await message.reply("База данных пуста. Добавьте продукты.")
    await message.reply("Добро пожаловать! Нажмите 'Рассчитать', чтобы узнать вашу норму калорий, или 'Информация', чтобы узнать больше.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Рассчитать")
async def main_menu(message: Message):
    await message.reply("Выберите опцию:", reply_markup=inline_keyboard)

@dp.message_handler(lambda message: message.text == "Регистрация")
async def sing_up(message: Message):
    await message.reply("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    username = message.text
    if crud_functions.is_included(username):
        await message.reply("Пользователь существует, введите другое имя.")
        return

    await state.update_data(username=username)
    await message.reply("Введите свой email:")
    await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.reply("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    age = message.text
    data = await state.get_data()
    username = data["username"]
    email = data["email"]

    try:
        age = int(age)
    except ValueError:
        await message.reply("Возраст должен быть числом. Попробуйте снова.")
        return

    crud_functions.add_user(username, email, age)
    await message.reply(f"Вы успешно зарегистрированы! Ваш баланс: 1000 ₽.")
    await state.finish()

@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.reply("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    weight = float(data["weight"])
    growth = float(data["growth"])
    age = int(data["age"])
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.reply(f"Ваша норма калорий: {calories:.2f} ккал")
    await state.finish()

@dp.message_handler(lambda message: message.text == "Информация")
async def information(message: Message):
    await message.reply("Этот бот помогает рассчитать вашу норму калорий. Нажмите 'Рассчитать', чтобы начать.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)