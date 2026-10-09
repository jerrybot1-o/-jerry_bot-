import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
TOTAL_MINED = 0
TOTAL_BURNED = 0
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = 0
    keyboard = [[InlineKeyboardButton("⛏️ MINE $JERRY", callback_data="mine")]]
    await update.message.reply_text(f"Welcome to $JERRY MINE 💎\nYour Balance: {users[user_id]}\nTOTAL_MINED: {TOTAL_MINED}\n0% burn now, 50% burn at launch!", reply_markup=InlineKeyboardMarkup(keyboard))

async def mine_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TOTAL_MINED
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    if uid not in users:
        users[uid] = 0
    users[uid] += 100
    TOTAL_MINED += 100
    keyboard = [[InlineKeyboardButton("⛏️ MINE AGAIN", callback_data="mine")]]
    await query.edit_message_text(f"⛏️ +100 $JERRY!\nYour Balance: {users[uid]}\nTotal Mined: {TOTAL_MINED}", reply_markup=InlineKeyboardMarkup(keyboard))

async def burn50(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TOTAL_MINED, TOTAL_BURNED
    burn_amt = TOTAL_MINED // 2
    TOTAL_MINED -= burn_amt
    TOTAL_BURNED += burn_amt
    await update.message.reply_text(f"🔥 50% BURN DONE!\nBurned: {burn_amt}\nRemaining: {TOTAL_MINED}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("burn50", burn50))
app.add_handler(CallbackQueryHandler(mine_btn))
app.run_polling()
