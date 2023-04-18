from aiogram.fsm.state import StatesGroup, State


class Start(StatesGroup):
    captcha_check = State()


class Add_staff(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()


class Staff(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()


class Staff2(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
