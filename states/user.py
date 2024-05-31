from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    lang = State()
    confirm = State()
    confirm_joined = State()

    menu = State()
    send_question = State()
    send_ticker = State()
    choose_question = State()
    premium = State()
    choose_tariff = State()



    payment = State()
    confirm_tariff = State()
    send_bill_check = State()




    admin = State()
    admin_channels = State()
    sendtousers = State()
    wait = State()
    addchannel = State()
    deletechannel = State()
    add_sums = State()

    enter_client_id = State()
    add_summa = State()
    manage_tariff = State()
    addtariff = State()
    addtariffdays = State()
    addtariffprice = State()
    deletetariff = State()

    get_tokens = State()
    enter_tariff = State()
    enter_count = State()
    remove_user = State()

    enter_token = State()

    choose_pages = State()
    choose_template = State()
    create_pres = State()
    create_abs = State()
    enter_abs_name = State()

    survey = State()
