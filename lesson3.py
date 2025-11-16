from random import choice
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final[str] = '8180287561:AAEI235cF4zV1zkcspl5WZozsC7T-zZKf3Y'
BOT_USERNAME: Final[str] = '@lesson3UA_bot'

# === 1. Команда /start ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_html(f"Привіт, {user.mention_html()}! 😄 Я навчальний бот. Напиши мені щось цікаве!")

# === 2. Команда /help ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html("Команди:\n/start — почати роботу\n/help — допомога\n/cat — випадкове фото котика 🐱")

# === 3. Нова команда /cat ===
async def cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cat_urls = [
        "https://cataas.com/cat",
        "https://placekitten.com/400/400",
        "https://cataas.com/cat/cute",
        "https://cataas.com/cat/says/Meow",
        "https://loremflickr.com/320/240/cat"
    ]
    await update.message.reply_photo(photo=choice(cat_urls), caption="Ось твій котик 😺")

# === 4. Відповіді на повідомлення ===
def handle_response(text: str) -> str:
    processed = text.lower()

    # Реакція на "привіт"
    if 'привіт' in processed:
        return 'O hello there! 👋'

    # Реакція на "python"
    elif 'python' in processed:
        return '🐍 Найкраща мова програмування!'

    # Реакція на "як ти"
    elif 'як ти' in processed:
        answers = [
            "Як Windows без оновлень — тримаюсь, але трохи глючу.",
            "Як котик у коробці — одночасно добре і загадково.",
            "Наче Wi-Fi: іноді стабільно, іноді взагалі без зв’язку.",
            "Живу, як Google Chrome: відкрито 100 вкладок, а батарея на нулі.",
            "Як морозиво в спеку — намагаюся не розтанути.",
        ]
        return choice(answers)

    # === 2. Реакція на "факт" / "цікавинка" / "цікаво" ===
    elif any(word in processed for word in ['факт', 'цікавинка', 'цікаво']):
        facts = [
            "🐝 Бджоли можуть розпізнавати людські обличчя!",
            "🐙 У восьминога три серця!",
            "🧠 Мозок людини споживає близько 20% енергії тіла.",
            "🦦 Морські видри сплять, тримаючись за лапки, щоб не розплистися.",
            "🌌 У космосі немає запахів — але скафандри після виходу пахнуть стейком!"
        ]
        return choice(facts)

    # === 1. Нова власна реакція ===
    elif 'жарт' in processed:
        jokes = [
            "— Що каже програміст, коли виходить з дому? — Logout 😎",
            "Мій код настільки хороший, що навіть компілятор аплодує (помилками).",
            "Я не лінивий — я просто працюю в режимі енергозбереження!",
            "Коли життя дає тобі помилки — дебагай їх 😉"
        ]
        return choice(jokes)

    return "W-what? sounds clever but I don’t get it 🤔"

# === 5. Обробка повідомлень ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.id} in {message_type}): "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print(f'Bot: {response}')
    await update.message.reply_text(response)

# === 6. Обробка помилок ===
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# === 7. Основна функція ===
def main():
    print('Starting up bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('cat', cat_command))  # 🐱 нова команда

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(handle_error)

    print('Polling...')
    app.run_polling(poll_interval=5)

if __name__ == '__main__':
    main()
