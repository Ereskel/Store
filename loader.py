from aiogram import Bot, Dispatcher, Router
from config import token

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher()

router1 = Router()