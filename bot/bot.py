from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from logic import add_game, add_book, delete_game_by_number, delete_book_by_number
from config import TOKEN

CHOOSING, ADD_GAME_NAME, ADD_GAME_IMAGE, ADD_GAME_DATE, ADD_BOOK_TITLE, ADD_BOOK_AUTHOR, ADD_BOOK_IMAGE, ADD_BOOK_YEAR, DELETE_GAME_NUMBER, DELETE_BOOK_NUMBER = range(10)
user_data = {}

def start(update: Update, context: CallbackContext):
    reply_keyboard = [
        ["Добавить игру", "Добавить книгу"],
        ["Удалить игру", "Удалить книгу"]
    ]
    update.message.reply_text(
        "📚 Привет! Что хотите сделать?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )
    return CHOOSING

def choose(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Добавить игру":
        update.message.reply_text("Название игры:")
        return ADD_GAME_NAME
    elif text == "Добавить книгу":
        update.message.reply_text("Название книги:")
        return ADD_BOOK_TITLE
    elif text == "Удалить игру":
        update.message.reply_text("Введите номер игры для удаления:")
        return DELETE_GAME_NUMBER
    elif text == "Удалить книгу":
        update.message.reply_text("Введите номер книги для удаления:")
        return DELETE_BOOK_NUMBER

def game_name(update: Update, context: CallbackContext):
    user_data["game_name"] = update.message.text
    update.message.reply_text("Ссылка на картинку игры:")
    return ADD_GAME_IMAGE

def game_image(update: Update, context: CallbackContext):
    user_data["game_image"] = update.message.text
    update.message.reply_text("Дата выхода игры:")
    return ADD_GAME_DATE

def game_date(update: Update, context: CallbackContext):
    add_game(user_data["game_name"], user_data["game_image"], update.message.text)
    update.message.reply_text("✅ Игра добавлена!")
    return start(update, context)

def book_title(update: Update, context: CallbackContext):
    user_data["book_title"] = update.message.text
    update.message.reply_text("Автор книги:")
    return ADD_BOOK_AUTHOR

def book_author(update: Update, context: CallbackContext):
    user_data["book_author"] = update.message.text
    update.message.reply_text("Ссылка на картинку книги:")
    return ADD_BOOK_IMAGE

def book_image(update: Update, context: CallbackContext):
    user_data["book_image"] = update.message.text
    update.message.reply_text("Год выпуска:")
    return ADD_BOOK_YEAR

def book_year(update: Update, context: CallbackContext):
    add_book(user_data["book_title"], user_data["book_author"], user_data["book_image"], update.message.text)
    update.message.reply_text("✅ Книга добавлена!")
    return start(update, context)

def delete_game_handler(update: Update, context: CallbackContext):
    try:
        number = int(update.message.text)
        delete_game_by_number(number)
        update.message.reply_text("🗑 Игра удалена.")
    except ValueError:
        update.message.reply_text("❗ Введите корректный номер.")
    return start(update, context)

def delete_book_handler(update: Update, context: CallbackContext):
    try:
        number = int(update.message.text)
        delete_book_by_number(number)
        update.message.reply_text("🗑 Книга удалена.")
    except ValueError:
        update.message.reply_text("❗ Введите корректный номер.")
    return start(update, context)

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Отменено.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex("^(Добавить игру|Добавить книгу|Удалить игру|Удалить книгу)$"), choose)],
            ADD_GAME_NAME: [MessageHandler(Filters.text & ~Filters.command, game_name)],
            ADD_GAME_IMAGE: [MessageHandler(Filters.text & ~Filters.command, game_image)],
            ADD_GAME_DATE: [MessageHandler(Filters.text & ~Filters.command, game_date)],
            ADD_BOOK_TITLE: [MessageHandler(Filters.text & ~Filters.command, book_title)],
            ADD_BOOK_AUTHOR: [MessageHandler(Filters.text & ~Filters.command, book_author)],
            ADD_BOOK_IMAGE: [MessageHandler(Filters.text & ~Filters.command, book_image)],
            ADD_BOOK_YEAR: [MessageHandler(Filters.text & ~Filters.command, book_year)],
            DELETE_GAME_NUMBER: [MessageHandler(Filters.text & ~Filters.command, delete_game_handler)],
            DELETE_BOOK_NUMBER: [MessageHandler(Filters.text & ~Filters.command, delete_book_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
