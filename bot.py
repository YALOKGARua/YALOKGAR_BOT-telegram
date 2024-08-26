import random
import requests
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from telegram.error import Forbidden

TOKEN = ''
WEATHER_API_KEY = ' '
WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json'

JOKES = [
    "Чому комп'ютер ніколи не відзначає свій день народження? Бо у нього вже є багато бітів!",
    "Як програмісти святкують Хелловін? Вони надягають костюм від '2-ох-місячної випробувальної версії'.",
    "Чому програміст ніколи не грає в хованки? Бо хороший програміст завжди залишає сліди!"
]

NEWS_API_KEY = ''
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

MOTIVATIONAL_QUOTES = [
    "Роби, що можеш, з тим, що маєш, там, де ти є.",
    "Ніколи не здавайся! Великі досягнення потребують часу.",
    "Життя — це те, що відбувається, поки ти плануєш інше."
]

important_dates = {
    '2024-08-26': 'Сьогодні важливий день для нашого бота!',
}

async def start(update: Update, context: CallbackContext):
    try:
        keyboard = [
            [InlineKeyboardButton("Отримати новини", callback_data='news')],
            [InlineKeyboardButton("Мотиваційна цитата", callback_data='quote')],
            [InlineKeyboardButton("Погода", callback_data='weather')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Привіт! Я ваш бот. Що ви хочете зробити?', reply_markup=reply_markup)
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def echo(update: Update, context: CallbackContext):
    try:
        if update.message.chat.type in ['group', 'supergroup']:
            if '@' + context.bot.username in update.message.text:
                await update.message.reply_text(update.message.text.replace('@' + context.bot.username, '').strip())
        else:
            await update.message.reply_text(update.message.text)
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def feedback(update: Update, context: CallbackContext):
    try:
        feedback_text = ' '.join(context.args)
        if feedback_text:
            with open('feedback.txt', 'a') as f:
                f.write(f"{update.effective_user.id}: {feedback_text}\n")
            await update.message.reply_text("Дякуємо за ваш відгук!")
        else:
            await update.message.reply_text("Будь ласка, вкажіть текст відгуку.")
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def joke(update: Update, context: CallbackContext):
    try:
        joke = random.choice(JOKES)
        await update.message.reply_text(joke)
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def weather(update: Update, context: CallbackContext):
    try:
        city = ' '.join(context.args)
        if not city:
            await update.message.reply_text("Будь ласка, вкажіть місто.")
            return
        
        response = requests.get(f"{WEATHER_API_URL}?key={WEATHER_API_KEY}&q={city}")
        data = response.json()
        
        if 'current' in data:
            weather_info = (
                f"Погода в місті {city}:\n"
                f"Температура: {data['current']['temp_c']}°C\n"
                f"Стан: {data['current']['condition']['text']}\n"
                f"Вологість: {data['current']['humidity']}%\n"
            )
            await update.message.reply_text(weather_info)
        else:
            await update.message.reply_text("Не вдалося отримати дані про погоду.")
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def check_dates(update: Update, context: CallbackContext):
    today = datetime.date.today().strftime('%Y-%m-%d')
    if today in important_dates:
        await update.message.reply_text(important_dates[today])
    else:
        await update.message.reply_text("Сьогодні немає важливих подій.")

async def set_language(update: Update, context: CallbackContext):
    try:
        new_language = context.args[0]
        if new_language in ['en', 'uk']:  # Example languages
            context.user_data['language'] = new_language
            await update.message.reply_text(f"Мова була змінена на {new_language}.")
        else:
            await update.message.reply_text("Невідома мова. Доступні: 'en', 'uk'.")
    except IndexError:
        await update.message.reply_text("Використання: /language <мова>")
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def news(update: Update, context: CallbackContext):
    try:
        response = requests.get(f"{NEWS_API_URL}?apiKey={NEWS_API_KEY}&country=us")
        data = response.json()
        
        if 'articles' in data and data['articles']:
            latest_news = data['articles'][0]
            news_info = (
                f"Останні новини:\n"
                f"Заголовок: {latest_news['title']}\n"
                f"Опис: {latest_news['description']}\n"
                f"Посилання: {latest_news['url']}\n"
            )
            if update.message:
                await update.message.reply_text(news_info)
            else:
                await update.callback_query.message.reply_text(news_info)
        else:
            if update.message:
                await update.message.reply_text("Не вдалося отримати новини.")
            else:
                await update.callback_query.message.reply_text("Не вдалося отримати новини.")
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def motivational_quote(update: Update, context: CallbackContext):
    try:
        quote = random.choice(MOTIVATIONAL_QUOTES)
        await update.message.reply_text(quote)
    except Forbidden:
        print(f"Бот був заблокований користувачем {update.effective_user.id}")

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'news':
        await news(update, context)
    elif query.data == 'quote':
        await motivational_quote(update, context)
    elif query.data == 'weather':
        await query.message.reply_text("Щоб дізнатися погоду, використовуйте команду /weather <місто>")

def main():
    application = Application.builder().token(TOKEN).build()

    try:
        job_queue = application.job_queue
    except AttributeError:
        job_queue = None
        print("JobQueue не доступний.")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("dates", check_dates))
    application.add_handler(CommandHandler("language", set_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()

if __name__ == '__main__':
    main()
