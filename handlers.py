import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from api import get_weather, get_news

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

LANGUAGES = {
    'en': {
        'start': 'Hello! I am your bot. What would you like to do?',
        'weather': 'To get the weather, use the command /weather <city>',
        'news': 'Here are the latest news:',
        'quote': 'Here is a motivational quote for you:',
        'feedback': 'Thank you for your feedback!',
        'language': 'Language has been changed to {}.'
    },
    'uk': {
        'start': 'Привіт! Я ваш бот. Що ви хочете зробити?',
        'weather': 'Щоб дізнатися погоду, використовуйте команду /weather <місто>',
        'news': 'Ось останні новини:',
        'quote': 'Ось мотиваційна цитата для вас:',
        'feedback': 'Дякуємо за ваш відгук!',
        'language': 'Мова була змінена на {}.'
    }
}

important_dates = {
    '2024-08-26': 'Сьогодні важливий день для нашого бота!',
}

async def start(update: Update, context: CallbackContext):
    user_language = context.user_data.get('language', 'en')
    text = LANGUAGES[user_language]['start']
    keyboard = [
        [InlineKeyboardButton("Get News", callback_data='news')],
        [InlineKeyboardButton("Motivational Quote", callback_data='quote')],
        [InlineKeyboardButton("Weather", callback_data='weather')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def echo(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.chat.type in ['group', 'supergroup']:
            if '@' + context.bot.username in update.message.text:
                await update.message.reply_text(update.message.text.replace('@' + context.bot.username, '').strip())
        elif update.message:
            await update.message.reply_text(update.message.text)
    except Exception as e:
        print(f"Error in echo: {e}")

async def feedback(update: Update, context: CallbackContext):
    try:
        feedback_text = ' '.join(context.args)
        if feedback_text:
            with open('feedback.txt', 'a') as f:
                f.write(f"{update.effective_user.id}: {feedback_text}\n")
            await update.message.reply_text(LANGUAGES.get(context.user_data.get('language', 'en'), 'feedback'))
        else:
            await update.message.reply_text("Будь ласка, вкажіть текст відгуку.")
    except Exception as e:
        print(f"Error in feedback: {e}")

async def joke(update: Update, context: CallbackContext):
    try:
        joke = random.choice(JOKES)
        await update.message.reply_text(joke)
    except Exception as e:
        print(f"Error in joke: {e}")

async def weather(update: Update, context: CallbackContext):
    try:
        city = ' '.join(context.args)
        if not city:
            await update.message.reply_text("Будь ласка, вкажіть місто.")
            return
        
        weather_info = get_weather(city)
        await update.message.reply_text(weather_info)
    except Exception as e:
        print(f"Error in weather: {e}")

async def check_dates(update: Update, context: CallbackContext):
    today = datetime.date.today().strftime('%Y-%m-%d')
    if today in important_dates:
        await update.message.reply_text(important_dates[today])
    else:
        await update.message.reply_text("Сьогодні немає важливих подій.")

async def set_language(update: Update, context: CallbackContext):
    try:
        new_language = context.args[0]
        if new_language in ['en', 'uk']:
            context.user_data['language'] = new_language
            await update.message.reply_text(LANGUAGES[new_language]['language'].format(new_language))
        else:
            await update.message.reply_text("Невідома мова. Доступні: 'en', 'uk'.")
    except IndexError:
        await update.message.reply_text("Використання: /language <мова>")
    except Exception as e:
        print(f"Error in set_language: {e}")

async def news(update: Update, context: CallbackContext):
    try:
        news_info = get_news()
        if update.message:
            await update.message.reply_text(news_info)
        elif update.callback_query:
            await update.callback_query.message.reply_text(news_info)
    except Exception as e:
        print(f"Error in news: {e}")

async def motivational_quote(update: Update, context: CallbackContext):
    try:
        quote = random.choice(MOTIVATIONAL_QUOTES)
        if update.message:
            await update.message.reply_text(quote)
        elif update.callback_query:
            await update.callback_query.message.reply_text(quote)
    except Exception as e:
        print(f"Error in motivational_quote: {e}")

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'news':
        await news(update, context)
    elif query.data == 'quote':
        await motivational_quote(update, context)
    elif query.data == 'weather':
        await query.message.reply_text("Щоб дізнатися погоду, використовуйте команду /weather <місто>")
