from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters

# Conversation states
NAME, DISTRICT, PHONE, MESSAGE = range(4)

async def start(update: Update, context: CallbackContext) -> int:
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(f"Ассалому алейкум, {user_first_name}!\n\nИсм Фамилияингизни ёзиб қолдиринг.")
    return NAME

async def get_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text

    districts = [
        ["Амударьё тумани", "Беруний тумани"],
        ["Бўзатов тумани", "Кегейли тумани"],
        ["Қонликўл тумани", "Қораўзак тумани"],
        ["Қўнғирот тумани", "Мўйноқ тумани"],
        ["Нукус тумани", "Нукус шахри"],
        ["Тахиатош тумани", "Тахтакўпир тумани"],
        ["Тўрткўл тумани", "Хўжайли тумани"],
        ["Чимбой тумани", "Шўманой тумани"],
        ["Элликқалъа тумани"]
    ]

    reply_markup = ReplyKeyboardMarkup(districts, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Илтимос, туманингизни танланг:", reply_markup=reply_markup)
    return DISTRICT

async def get_district(update: Update, context: CallbackContext) -> int:
    context.user_data['district'] = update.message.text

    button = KeyboardButton("Телефон рақамни улашиш", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Илтимос, телефон рақамингизни қолдиринг:", reply_markup=reply_markup)
    return PHONE

async def get_phone(update: Update, context: CallbackContext) -> int:
    contact = update.message.contact
    if contact:
        context.user_data['phone'] = contact.phone_number
        await update.message.reply_text("Мурожаатингизнинг қисқача мазмунини ёзиб қолдиринг.")
        return MESSAGE
    else:
        await update.message.reply_text("Телефон рақамини улашишда хатолик юз берди. Илтимос, қайта уриниб кўринг.")
        return PHONE

async def get_message(update: Update, context: CallbackContext) -> int:
    context.user_data['message'] = update.message.text

    user_data = context.user_data
    response = (("Рахмат! Қуйидаги маълумотларингиз қабул қилинди:\n\n"
                f"👤 Исм, Фамилия: {user_data['name']}\n"
                f"📍 Туман: {user_data['district']}\n"
                f"📞 Телефон: {user_data['phone']}\n"
                f"✉️ Мурожаат мазмуни: {user_data['message']}"))

    await update.message.reply_text(response)
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Jarayon bekor qilindi.")
    return ConversationHandler.END

def main() -> None:
    TOKEN = "7626894370:AAEnQs-BRsPAwJezYqiSdMDDcia_Rh7zgJM"
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_district)],
            PHONE: [MessageHandler(filters.CONTACT, get_phone)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
