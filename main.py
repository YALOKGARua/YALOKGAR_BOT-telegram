from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers import start, feedback, joke, weather, check_dates, set_language, news, motivational_quote, button, echo

def main():
    application = Application.builder().token('7355619387:AAF0Dy9YKnNMk5jj9ANlEdwmUHoCPv1BjRo').build()

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
