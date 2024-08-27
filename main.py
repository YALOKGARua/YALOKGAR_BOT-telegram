import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from telegram.error import Forbidden
from api import get_weather, get_news

TOKEN = '7355619387:AAF0Dy9YKnNMk5jj9ANlEdwmUHoCPv1BjRo'

JOKES = [
    "Чому комп'ютер ніколи не відзначає свій день народження? Бо у нього вже є багато бітів!",
    "Як програмісти святкують Хелловін? Вони надягають костюм від '2-ох-місячної випробувальної версії'.",
    "Чому програміст ніколи не грає в хованки? Бо хороший програміст завжди залишає сліди!"
]

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
        
        weather_info = get_weather(city)
        await update.message.reply_text(weather_info)
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
        news_info = get_news()
        if update.message:
            await update.message.reply_text(news_info)
        else:
            await update.callback_query.message.reply_text(news_info)
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
