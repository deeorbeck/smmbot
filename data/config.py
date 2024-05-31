from environs import Env

env = Env()
env.read_env()
pro = env.bool('PRODUCTION')
BOT_TOKEN = env.str("BOT_TOKEN") if pro else env.str("TEST_BOT_TOKEN")
SUPER_ADMIN = env.int("SUPER_ADMIN")
ADMINS = [SUPER_ADMIN] + env.list("ADMINS")
GROUP_ID = env.str("GROUP_ID")
card = env.str('CARD')
admin_username = env.str("ADMIN_USERNAME")
SMM_API_KEY = env.str("SMM_API_KEY")
SMM_API_URL = env.str("SMM_API_URL")
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.int("DB_PORT")

main_lang = 'uz'
langs = {
    "🇺🇿O'zbekcha": 'uz',
	"🇬🇧English": 'en',
    "🇷🇺Русский": 'ru',
}
default_sums = 10000
sums_per_reffer = 5000


class Texts:
	def __init__(self, lang=None):
		self.lang = lang or main_lang
	def yes_no(self):
		return {
			'uz': ["✅Ha", "❌Yo'q"],
			'en': ["✅Yes", "❌No"],
			'ru': ["✅Да", "❌Нет"]
		}[self.lang]
	def contact(self):
		return {
			'uz': f"👨🏻‍💻Admin: {admin_username}",
			'en': f"👨🏻‍💻Admin: {admin_username}",
			'ru': f"👨🏻‍💻Администратор: {admin_username}"
		}[self.lang]
	def get_balance(self):
		return {
			'uz': "💸Sizning balansingiz: {} so'm",
			'en': "💸Your balance: {} soum",
			'ru': "💸Ваш баланс: {} сум"
		}[self.lang]
	def annotation_text(self):
		return {
			'uz': "ANNOTATSIYA",
			'en': "ANNOTATION",
			'ru': "АННОТАЦИЯ"
		}[self.lang]
	def key_words_text(self):
		return {
			'uz': "Kalit so'zlar",
			'en': "Key words",
			'ru': "Ключевые слова"
		}[self.lang]
	def conclusion_text(self):
		return {
			'uz': "Xulosa",
			'en': "Conclusion",
			'ru': "Заключение"
		}[self.lang]
	def references_text(self):
		return {
			'uz': "Foydalanilgan adabiyotlar",
			'en': "References",
			'ru': "Рекомендации"
		}[self.lang]
	def survey(self):
		return {
			'uz': "Assalomu alaykum ",
			'en': "💸Your balance: {} soum",
			'ru': "💸Ваш баланс: {} сум"
		}[self.lang]

	def ignore_payment_check(self):
		return {
			'uz': "Iltimos, to'g'ri chekni yuboring!",
			'en': "Please send the correct check!",
			'ru': "Пожалуйста, пришлите правильный чек!"
		}[self.lang]
	def send_only_photo(self):
		return {
			'uz': "Faqat rasm yoki fayl ko'rinishida yuboring!",
			'en': "Send as an image or file only!",
			'ru': "Отправляйте только в виде изображения или файла!"
		}[self.lang]
	def wait_confirm(self):
		return {
			'uz': "To'lov cheki qabul qilindi.\nIltimos admin javobini kuting...\nNoqulaylik uchun {} gamurojaat qiling.",
			'en': "Payment check received.\nPlease wait for admin response...\nSorry {} for the inconvenience.",
			'ru': "Чек о платеже получен.\nПожалуйста, подождите ответа администратора...\nПриносим {} извинения за неудобства."
		}[self.lang]
	def admin_confirmed(self):
		return {
			'uz': "✅To'lovingiz qabul qilindi!\n💸Hisobingizda {} so'm mavjud.",
			'en': "✅Your payment has been accepted!\n💸You have {} soums in your account.",
			'ru': "✅Ваш платеж принят!\n💸У вас на счету {} сумов."
		}[self.lang]
	def send_check(self):
		return {
			'uz': f"Ushbu kartaga to'lov qiling va chekni botga yuboring👇\n{card}",
			'en': f"Pay to this card and send the check to the bot👇\n{card}",
			'ru': f"Оплатите на эту карту и отправьте чек боту👇\n{card}"
		}[self.lang]
	def take_payment(self):
		return {
			'uz': "💳To'lov qilish",
			'en': "💳Payment",
			'ru': "💳Оплата"

		}[self.lang]
	def thanks(self):
		return {
			'uz': "E'tiboringiz uchun rahmat",
			'en': "Thank you for your attention",
			'ru': "Спасибо за внимание"

		}[self.lang]
	def promoteadminbot(self):
		return {
			'uz': "Kanalni qo'shishdan avval botni unga admin qilib tayinlang!",
			'en': "Promote your bot an admin of channel before adding a channels list!",
			'ru': "Прежде чем добавлять канал, сделайте своего бота администратором!"

		}[self.lang]
	def appendchannel(self):
		return {
			'uz': "{} qo'shildi",
			'en': "{} added",
			'ru': "{} добавлен"

		}[self.lang]
	def deletechannel(self):
		return {
			'uz': "{} kanal o'chirildi",
			'en': "{} channel deleted",
			'ru': "{} канал удален"

		}[self.lang]
	def enterchannel_id(self):
		return {
			'uz': "Kanal id sini yuboring: ",
			'en': "Send channel id:",
			'ru': "Отправить идентификатор канала:"

		}[self.lang]
	def beforemustsubscribe(self):
		return {
			'uz': "❌Avval quyidagi kannallarga ubuna bo'ling!👇",
			'en': "❌Subscribe to the following channels first!👇",
			'ru': "❌Сначала подпишитесь на следующие каналы!👇"

		}[self.lang]
	def subscibed(self):
		return {
			'uz': "🛎Obuna bo'ldim",
			'en': "🛎I subscribed",
			'ru': "🛎Я подписался"

		}[self.lang]
	def didntfoundticker(self):
		return {
			'uz': '❌Aksiya topilmadi',
			'en': "❌The stock not found",
			'ru': "❌Акция не найдена"

		}[self.lang]
	def ticker_complience(self):
		return {
			'uz': '🌙Aksiya halolligini tekshirish',
			'en': "🌙Check the compliance of the stock",
			'ru': "🌙Проверьте честность продвижения"

		}[self.lang]


	def completly_started(self):
		return {
			'uz': '✨Siz botdan muvaffaqiyatli ro\'yxatdan o\'tdingiz va {} so\'mga ega bo\'ldingiz! ',
			'en': "✨You have successfully registered from the bot and received {} soums!",
			'ru': "✨Вы успешно зарегистрировались у бота и получили {} сумов!"

		}[self.lang]


	def main(self):
		return {
			'uz': '🔝Bosh sahifa',
			'en': "🔝Main page",
			'ru': "🔙Главная страница"

		}[self.lang]
	def orqaga(self):
		return {
			'uz': '🔙Orqaga',
			'en': "🔙Back",
			'ru': "🔙Назад"

		}[self.lang]
	def phone_number(self):
		text = {
		'uz': 'Telefon raqamingizni ulashish uchun: "📲Raqamni yuborish" tugmasini bosing',
		'en': 'To share your phone number: Click the "📲Send" button',
		'ru': "Чтобы поделиться своим номером телефона: нажмите кнопку 📲Отправить"
		}
		return text[self.lang]

	def phone_number_button(self):
		text = {
		'uz': "📱Yuborish",
		'en': "📱Send",
		'ru': "📱 Отправить"
		}
		return text[self.lang]

	def choose(self):
		text = {
		'uz': 'Tanlang👇',
		'ru': "Выбирайте👇",
		'en': "Choose👇"
		}
		return text[self.lang]
	def user_sections(self):
		text = {
			'uz': [
				"⚡️SMM xizmatlari",
				"🗂Buyurtmalarim",
				"💸Hisobni to'ldirish",
				"🔗Refferal",
				"👨🏻‍💻Bog'lanish"
			],
			'en': [
				"⚡️SMM services",
				"🗂My orders",
				"💸Top up account",
				"🔗Referral",
				"👨🏻‍💻Contact"
			],
			'ru': [
				"⚡️SMM-услуги",
				"🗂Мои заказы",
				"💸Пополнить счет",
				"🔗Реферал",
				"👨🏻‍💻Контакт"
			]
		}
		return text[self.lang]
	def refferal_successful_text(self):
		text = {
			'uz': "Siz <b>{}</b> ni botga taklif qildingiz💫\nVa {} so'mga ega bo'ldingiz🎉",
			'en': "You invited <b>{}</b> to the bot💫\nAnd you got {} sums🎉",
			'ru': "Вы пригласили <b>{}</b> в бот💫\nИ у тебя есть {} сум🎉",
		}
		return text[self.lang]
	def changed_access_time_via_refferal(self):
		text = {
			'uz': "Siz taklif qilgan foydalanuvchilar soni {} ga yetdi.\nVa siz {} gacha botdan foydalanish huquqiga ega bo'ldingiz.",
			'en': "The number of users you have invited has reached {}.\nAnd you have access to the bot up to {}.",
			'ru': "Число приглашенных вами пользователей достигло {}.\nИ у вас есть доступ к боту до {}.",
		}
		return text[self.lang]
	def confirm_pres(self):
		text = {
			'uz': "📎Mavzu: {}\nSlaydlar soni: {}\nTasdiqlaysizmi? ",
			'en': "📎Topic: {}\nNumber of slides: {}\nDo you approve?",
			'ru': "📎Тема: {}\nКоличество слайдов: {}\nВы одобряете?"
		}
		return text[self.lang]
	def choose_template(self):
		text = {
			'uz': "🧩Taqdimot uchun shablon tanlang",
			'en': "🧩Choose a template for the presentation",
			'ru': "🧩Выберите шаблон для презентации"
		}
		return text[self.lang]
	def choose_pages_count(self):
		text = {
			'uz': "🎲Taqdimot sahifalari sonini tanlang",
			'en': "🎲Выберите количество страниц презентации",
			'ru': "🎲Select the number of presentation pages"
		}
		return text[self.lang]
	def send_theme_of_pres(self):
		text = {
			'uz': "Taqdimot mavzusini yuboring👇",
			'en': "Send the topic of the presentation👇",
			'ru': "Присылайте тему презентации👇"
		}
		return text[self.lang]


	def send_ticker(self):
		return {
			'uz': 'Quyida siz aksiya tikerini $ belgisi bilan kiriting! Masalan: $AAPL yoki $aapl ko`rinishida.👇',
			'en': "Below you enter the stock ticker with the $ sign! For example: $AAPL or $aapl.👇",
			'ru': "Ниже вы вводите тикер акции со знаком $! Например: $AAPL или $aapl.👇"

		}[self.lang]
	def waiting_generate(self):
		return {
			'uz': '♻️Kuting javob tayyorlanmoqda...',
			'en': "♻️Please wait for a response...",
			'ru': "♻️Пожалуйста, дождитесь ответа..."

		}[self.lang]
	def choose_one(self):
		return {
			'uz': "Savollardan birini tanlang👇",
			'en': "Choose one of the questions👇",
			'ru': "Выберите один из вопросов👇"
		}[self.lang]
	def premium_sections(self):
		return {
			'uz': [ '📲Referal tizimi'],
			'en': [ '📲Referral System'],
			"ru": ['📲Реферальная система']
		}[self.lang]
	def your_refferal_link(self):
		return {
			'uz': f"Sizning referralingiz orqali qo'shilgan 1 kishi uchun {sums_per_reffer} so'm olasiz.\n✨Sizning refferal havolangiz👇",
			'en': f'You will get {sums_per_reffer} soums for 1 person who joins through your referral.\n✨Your referral link👇',
			"ru": f'Вы получите {sums_per_reffer} сумов за 1 человека, который присоединится по вашему рефералу.\n✨Ваша реферальная ссылка👇'
		}[self.lang]

	def refferal_link(self):
		return {
			'uz': "Sun'iy intellekt orqali tekinga prezentatsiya tayyorlang.\nSinab ko'rish👉🏻 https://t.me/{}",
			'en': 'Create a free presentation using artificial intelligence.\nTry it👉🏻 https://t.me/{}',
			"ru": 'Создайте бесплатную презентацию с помощью искусственного интеллекта.\nПопробуйте👉🏻 https://t.me/{}'
		}[self.lang]
	def choose_tariff(self):
		return {
			'uz': 'Quyidagi tariflardan birini tanlang',
			'en': 'Choose one of the rates below',
			"ru": 'Выберите один из тарифов ниже'
		}[self.lang]
	def choose_tariff_to_using(self):
		return {
			'uz': '💸Botdan foydalanishda davom etish uchun tariflar bilan tanishing👇\nYoki {} tomonidan berilgan bir martalik <b><i>token</i></b>ni yuboring',
			'en': '💸Read the rates to continue using the bot👇\nOr send a one-time <b><i>token</i></b> issued by {}',
			"ru": '💸Прочитайте тарифы, чтобы продолжить использование бота👇\nИли отправьте одноразовый <b><i>токен</i></b>, выпущенный {}'
		}[self.lang]
	def tariff_info(self):
		return {
			'uz': '<b>{}</b>  obuna narxi <b>{}</b> so\'m\nMaxsus token olish uchun '+ admin_username +' ga yozing',
			'en': '<b>{}</b>  subscription price <b>{}</b> sum\nTo get a special token, write to ' + admin_username,
			"ru": '<b>{}</b>  стоимость подписки <b>{}</b> sum\nЧтобы получить специальный токен, напишите ' + admin_username
		}[self.lang]
	def enter_token_text(self):
		return {
			'uz': '👨🏻‍💻Admin bergan tokenni kiritish',
			'en': '👨🏻‍💻Enter the token given by the admin',
			'ru': '👨🏻‍💻Введите токен, предоставленный администратором',
		}[self.lang]
	def ignore_token_text(self):
		return {
			'uz': """Afsuski, ushbu TOKEN raqam bizning  bazamizda mavjud emas yoki siz allaqachon ishlatilgan TOKEN raqamni kiritmoqdasiz.""",
			'en': 'Unfortunately, this TOKEN number is not available in our database, or you are entering a TOKEN number that has already been used.',
			'ru': 'К сожалению, этот номер ТОКЕНА недоступен в нашей базе данных, или вы вводите номер ТОКЕНА, который уже использовался.',
		}[self.lang]
	def admin_sections(self):
		return {
			'uz':  [
				"💰Balansni to'ldirish",


				"📲Foydalanuvchilarga xabar yuborish",
				"📊Statistika",

				"📃Mavjud tokenlar",
				"♻️Yangi generatsiya qilish",
				"🗑Foydalanuvchini o'chirish",
				"👨🏻‍💻Kanallar boshqaruvi",
			],
			'en': [
				"💰Rate Management",


				"📲Send messages to users",
				"📊Statistics",

				"📃Available Tokens",
				"♻️Making a new generation",
				"🗑Delete User",
				"👨🏻‍💻Channel Management",
			],
			'ru': [
				"💰Управление тарифами",
				

				"📲Отправлять сообщения пользователям",
				"📊Статистика",
				
				"📃Доступные токены",
				"♻️Создаем новое поколение",
				"🗑Удалить пользователя",
				"👨🏻‍💻Управление каналом",
			]
		}[self.lang]
	def send_post_to_rek(self):
		return {
			'uz': "Kontentni yuboring",
			'en': "Send content",
			'ru': "Отправить контент",
		}[self.lang]
	def count_users(self):
		return {
			'uz': "📊Foydalanuvchilar soni: {}",
			'en': "📊Number of users: {}",
			'ru': "📊Количество пользователей: {}",
		}[self.lang]
	def send_user_id(self):
		return {
			'uz': "Foydalanuvchi ID sini kiriting👇",
			'en': "Enter User ID👇",
			'ru': "Введите идентификатор пользователя👇",
		}[self.lang]
	def enter_tokens_count(self):
		return {
			'uz': "Yaratmoqchi bo'lgan tokenlaringiz miqdorini kiring",
			'en': "Enter the amount of tokens you want to generate",
			'ru': "Введите количество токенов, которое вы хотите сгенерировать",
		}[self.lang]
	def enter_true_count(self):
		return {
			'uz': "Son kiriting!\nMisol uchun <i>20</i>",
			'en': "Enter a number!\nFor example <i>20</i>",
			'ru': "Введите число!\nНапример, <i>20</i>",
		}[self.lang]
	def admin_panel_text(self):
		return {
			'uz': "Admin panel",
			'en': "Admin panel",
			'ru': "Панель администратора",
		}[self.lang]
	def not_founded_user_text(self):
		return {
			'uz': "Foydalanuvchi topilmadi!",
			'en': "User not found!",
			'ru': "Пользователь не найден!",
		}[self.lang]
	def user_deleted_successfully(self):
		return {
			'uz': "Muvaffaqiyatli o'chirildi✅",
			'en': "Deleted successfully✅",
			'ru': "Удален успешно✅",
		}[self.lang]
	def sent_users_count(self):
		return {
			'uz': "{} ta foydalanuvchilarga yuborildi:)",
			'en': "Sent to {} users:)",
			'ru': "Отправлено {} пользователям:)",
		}[self.lang]
	def enter_tariff_name(self):
		return {
			'uz': "Tarifga nom bering misol uchun \n<i>6 oylik</i>",
			'en': "Name the tariff, for example \n<i>6 months</i>",
			'ru': "Назовите тариф, например \n<i>6 месяцев</i>",
		}[self.lang]
	def tariff_name_price(self):
		return {
			'uz': "Tarif nomi: <b>{} ({} kun)</b>\nNarxi: <b>{} so'm</b>",
			'en': "Tariff name: <b>{} ({} day)</b> \nPrice: <b>{} sum</b>",
			'ru': "Название тарифа: <b>{} ({} день)</b>\nЦена: <b>{} сум</b>",
		}[self.lang]
	def enter_days_count(self):
		return {
			'uz': "Kun miqdorini kiriting misol uchun 6 oy uchun <i>180</i> kun👇",
			'en': "Enter the number of days, for example <i>180</i> days for 6 months👇",
			'ru': "Введите количество дней, например <i>180</i> дней для 6 месяцев👇",
		}[self.lang]
	def enter_only_numbers(self):
		return {
			'uz': "Kun miqodori faqat raqamlardan iborat bo'lishi kerak\nIltimos <i>180  360</i> kabi sonlardan foydalaning!",
			'en': "The amount of days must be numbers only\nPlease use numbers like <i>180 360</i>!",
			'ru': "Количество дней должно быть только числами.\nПожалуйста, используйте цифры, например <i>180 360</i>!",
		}[self.lang]
	def enter_tariff_price(self):
		return {
			'uz': "Oxirgi bosqich: Tarif narxini kiriting misol uchun \n<i>1200</i>\nSo'm so'zi shart emas 👇",
			'en': "Last step: Enter the price of the tariff, for example \n<i>1200</i>\nSoum is not necessary 👇",
			'ru': "Последний шаг: Введите стоимость тарифа, например \n<i>1200</i>\nСум не обязательно 👇",
		}[self.lang]
	def appended_tariff_text(self):
		return {
			'uz': '<i>"{}"</i> tarifi muvaffaqiyatli qo\'shildi',
			'en': '<i>"{}"</i> tariff added successfully',
			'ru': 'Тариф <i>"{}"</i> успешно добавлен',
		}[self.lang]
	def enter_token_by_admin(self):
		return {
			'uz': 'Tokenni kiriting👇',
			'en': 'Enter the token👇',
			'ru': 'Введите токен👇',
		}[self.lang]

	def changed_access_time(self):
		return {
			'uz': "✅Bot uchun ruxsat {}.{}.{} gacha uzaytirildi",
			'en': '✅Bot permission extended to {}.{}.{}',
			'ru': '✅Разрешение бота расширено до {}.{}.{}',
		}[self.lang]
