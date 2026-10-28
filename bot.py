import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set.")

def main_menu():
    keyboard = [
        ["👑 Тарихи тұлғалар", "🏛️ Тарихи орындар"],
        ["📅 Маңызды даталар", "💡 Қызықты фактілер"],
        ["🎮 Тарихи Quiz", "📖 Дереккөздер"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_active"] = False
    context.user_data["question"] = 0
    context.user_data["score"] = 0
    await update.message.reply_text(
        "🇰🇿 *TARIHBOT*\\n\\n"
        "Қазақстан тарихын заманауи әрі қызықты "
        "форматта танытатын студенттік жоба.\\n\\n"
        "Төмендегі бөлімдердің бірін таңдаңыз 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )

async def figures_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["👑 Керей хан", "👑 Жәнібек хан"],
        ["👑 Қасым хан", "👑 Тәуке хан"],
        ["👑 Абылай хан"],
        ["🔙 Басты мәзір"],
    ]
    await update.message.reply_text(
        "👑 *Тарихи тұлғаны таңдаңыз:*",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

async def places_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🏛️ Ясауи кесенесі", "🏺 Отырар"],
        ["🪨 Тамғалы", "🏙️ Сарайшық"],
        ["🔙 Басты мәзір"],
    ]
    await update.message.reply_text(
        "🏛️ *Тарихи орынды таңдаңыз:*",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

figures = {
    "👑 Керей хан": (
        "👑 *Керей хан*\\n\\n"
        "Керей хан — Қазақ хандығының алғашқы хандарының бірі. "
        "Қазақ хандығының құрылуы Керей мен Жәнібек "
        "сұлтандардың есімдерімен байланысты."
    ),
    "👑 Жәнібек хан": (
        "👑 *Жәнібек хан*\\n\\n"
        "Жәнібек хан — Қазақ хандығының қалыптасуында "
        "маңызды рөл атқарған тарихи тұлға. "
        "Ол Керей ханмен бірге Қазақ хандығының негізін қалаған."
    ),
    "👑 Қасым хан": (
        "👑 *Қасым хан*\\n\\n"
        "Қасым хан тұсында Қазақ хандығының саяси "
        "ықпалы күшейді. Оның есімі "
        "«Қасым ханның қасқа жолы» заңдар жүйесімен байланысты."
    ),
    "👑 Тәуке хан": (
        "👑 *Тәуке хан*\\n\\n"
        "Тәуке хан қазақ мемлекеттілігінің тарихындағы "
        "маңызды тұлғалардың бірі. Оның тұсында "
        "«Жеті жарғы» заңдар жинағы жүйеленді."
    ),
    "👑 Абылай хан": (
        "👑 *Абылай хан*\\n\\n"
        "Абылай хан XVIII ғасырдағы қазақ тарихындағы "
        "аса маңызды тұлғалардың бірі. "
        "Ол қазақ жерінің тұтастығын сақтауға "
        "және сыртқы саяси байланыстарды нығайтуға күш салды."
    ),
}

places = {
    "🏛️ Ясауи кесенесі": (
        "🏛️ *Қожа Ахмет Ясауи кесенесі*\\n\\n"
        "Кесене Түркістан қаласында орналасқан. "
        "Ол XIV ғасырдың соңында Әмір Темірдің "
        "бұйрығымен салынған.\\n\\n"
        "Бұл — Қазақстанның маңызды тарихи-мәдени "
        "ескерткіштерінің бірі."
    ),
    "🏺 Отырар": (
        "🏺 *Отырар қалашығы*\\n\\n"
        "Отырар — Қазақстанның оңтүстігіндегі "
        "ортағасырлық ірі қалалардың бірі.\\n\\n"
        "Ол Ұлы Жібек жолы бойындағы маңызды "
        "сауда және мәдени орталық болған."
    ),
    "🪨 Тамғалы": (
        "🪨 *Тамғалы петроглифтері*\\n\\n"
        "Тамғалы археологиялық ландшафты "
        "ежелгі жартас суреттерімен белгілі.\\n\\n"
        "Петроглифтер ежелгі адамдардың мәдениеті "
        "мен дүниетанымы туралы ақпарат береді."
    ),
    "🏙️ Сарайшық": (
        "🏙️ *Сарайшық қалашығы*\\n\\n"
        "Сарайшық — Батыс Қазақстандағы "
        "ортағасырлық тарихи қала орны.\\n\\n"
        "Ол Алтын Орда және кейінгі қазақ "
        "тарихымен байланысты."
    ),
}

async def dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 *Қазақстан тарихындағы маңызды даталар*\\n\\n"
        "🏰 *1465–1466 жж.*\\nҚазақ хандығының құрылу кезеңі.\\n\\n"
        "⚔️ *1723 ж.*\\n«Ақтабан шұбырынды, Алқакөл сұлама» "
        "оқиғалары басталған кезең.\\n\\n"
        "📜 *1731 ж.*\\nКіші жүздің Ресей империясымен байланысының "
        "жаңа кезеңі басталды.\\n\\n"
        "⭐ *1917 ж.*\\nАлаш қозғалысының маңызды тарихи кезеңі.\\n\\n"
        "🇰🇿 *1991 ж. 16 желтоқсан*\\nҚазақстан Республикасының мемлекеттік "
        "тәуелсіздігі туралы заң қабылданды.",
        parse_mode="Markdown",
    )

async def facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 *Қызықты фактілер*\\n\\n"
        "1️⃣ Қазақ хандығының қалыптасуы Керей мен Жәнібек есімдерімен байланысты.\\n\\n"
        "2️⃣ Түркістан — қазақ халқының маңызды тарихи және рухани орталықтарының бірі.\\n\\n"
        "3️⃣ Отырар Ұлы Жібек жолындағы маңызды қалалардың бірі болған.\\n\\n"
        "4️⃣ Тамғалыдағы петроглифтер ежелгі дәуірдің мәдени мұрасын көрсетеді.\\n\\n"
        "5️⃣ Қазақстан 1991 жылы тәуелсіз мемлекет болды.",
        parse_mode="Markdown",
    )

async def sources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Пайдаланылған дереккөздер*\\n\\n"
        "• Қазақстан тарихы бойынша университеттік оқулықтар\\n"
        "• Қазақстан Республикасының ресми материалдары\\n"
        "• UNESCO World Heritage материалдары\\n"
        "• Қазақстанның тарихи-мәдени мұрасы туралы ғылыми еңбектер\\n\\n"
        "⚠️ Жоба қорғауға дейін барлық тарихи мәліметтерді нақты дереккөздермен тексеріңіздер.",
        parse_mode="Markdown",
    )

quiz = [
    {"q": "Қазақ хандығының негізін қалаған хандар кімдер?",
     "a": ["A) Абылай мен Тәуке", "B) Керей мен Жәнібек", "C) Қасым мен Хақназар", "D) Есім мен Тәуке"], "correct": "B"},
    {"q": "Қазақ хандығының құрылуы қай кезеңмен байланысты?",
     "a": ["A) 1465–1466", "B) 1600–1601", "C) 1700–1701", "D) 1800–1801"], "correct": "A"},
    {"q": "Қожа Ахмет Ясауи кесенесі қай қалада орналасқан?",
     "a": ["A) Алматы", "B) Тараз", "C) Түркістан", "D) Астана"], "correct": "C"},
    {"q": "«Жеті жарғы» қай ханның тұсында жүйеленді?",
     "a": ["A) Тәуке хан", "B) Абылай хан", "C) Қасым хан", "D) Керей хан"], "correct": "A"},
    {"q": "Қазақстан тәуелсіздігін қай жылы жариялады?",
     "a": ["A) 1986", "B) 1990", "C) 1991", "D) 1995"], "correct": "C"},
    {"q": "Қазақстанның Тәуелсіздік күні қай күн?",
     "a": ["A) 1 желтоқсан", "B) 16 желтоқсан", "C) 25 қазан", "D) 30 тамыз"], "correct": "B"},
    {"q": "Қазақ хандығының алғашқы хандарының бірі кім?",
     "a": ["A) Керей хан", "B) Абылай хан", "C) Тәуке хан", "D) Әбілқайыр хан"], "correct": "A"},
    {"q": "Тамғалы немен танымал?",
     "a": ["A) Сарайларымен", "B) Петроглифтерімен", "C) Порттарымен", "D) Заманауи ғимараттарымен"], "correct": "B"},
    {"q": "Абылай хан қай ғасырдағы тарихта маңызды тұлға болды?",
     "a": ["A) XV ғасыр", "B) XVI ғасыр", "C) XVIII ғасыр", "D) XX ғасыр"], "correct": "C"},
    {"q": "Алаш қозғалысы қай ғасырдың басындағы тарихпен байланысты?",
     "a": ["A) XV ғасыр", "B) XVIII ғасыр", "C) XIX ғасыр", "D) XX ғасыр"], "correct": "D"},
]

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = context.user_data["question"]
    if number >= len(quiz):
        score = context.user_data["score"]
        context.user_data["quiz_active"] = False
        await update.message.reply_text(
            f"🏆 *QUIZ АЯҚТАЛДЫ!*\n\nСіздің нәтижеңіз:\n\n"
            f"⭐ *{score} / {len(quiz)}*\n\nТарихты зерттеуді жалғастырыңыз! 🇰🇿",
            reply_markup=main_menu(),
            parse_mode="Markdown",
        )
        return
    current = quiz[number]
    keyboard = [[answer] for answer in current["a"]]
    await update.message.reply_text(
        f"🎮 *Сұрақ {number + 1}/{len(quiz)}*\n\n{current['q']}",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_active"] = True
    context.user_data["question"] = 0
    context.user_data["score"] = 0
    await send_question(update, context)

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = context.user_data["question"]
    current = quiz[number]
    user_answer = update.message.text[0]
    if user_answer == current["correct"]:
        context.user_data["score"] += 1
        await update.message.reply_text("✅ Дұрыс жауап! 🎉")
    else:
        await update.message.reply_text(
            f"❌ Қате жауап.\nДұрыс жауап: {current['correct']}"
        )
    context.user_data["question"] += 1
    await send_question(update, context)

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("quiz_active", False):
        if text.startswith(("A)", "B)", "C)", "D)")):
            await check_answer(update, context)
            return

    if text == "🔙 Басты мәзір":
        await start(update, context)
    elif text == "👑 Тарихи тұлғалар":
        await figures_menu(update, context)
    elif text == "🏛️ Тарихи орындар":
        await places_menu(update, context)
    elif text == "📅 Маңызды даталар":
        await dates(update, context)
    elif text == "💡 Қызықты фактілер":
        await facts(update, context)
    elif text == "📖 Дереккөздер":
        await sources(update, context)
    elif text == "🎮 Тарихи Quiz":
        await start_quiz(update, context)
    elif text in figures:
        await update.message.reply_text(figures[text], parse_mode="Markdown")
    elif text in places:
        await update.message.reply_text(places[text], parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "🤔 Бөлімді түсінбедім.\n\nМәзірден таңдаңыз 👇",
            reply_markup=main_menu(),
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))
    print("TARIHBOT іске қосылды.")
    app.run_polling()

if __name__ == "__main__":
    main()
