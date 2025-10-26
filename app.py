import os
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== CONFIG ==========
SPREADSHEET_ID = '19ttgTtnU1AZyTwNmiafSGiQx6R3hJqhemqioIkwaSYM'
RANGE_NAME = 'Sheet1!A:C'  # assuming columns: Date, Category, Amount
TOKEN = '7930593247:AAHlZo5V11LlG-bK8YO8Lu9MCFwYUBSFudg'
CREDENTIALS_FILE = '"E:\programming\python projects\api keys\silent-cider-459817-q7-ded5fe07600b.json"'

# ========== GOOGLE SHEETS AUTH ==========
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)

# ========== FUNCTION TO FETCH DATA ==========
def fetch_data_from_sheets():
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    data = []
    for row in values[1:]:  # Skip header
        try:
            date = datetime.strptime(row[0], '%Y-%m-%d')
            category = row[1]
            amount = float(row[2])
            data.append({'date': date, 'category': category, 'amount': amount})
        except:
            continue
    return data

# ========== FUNCTION TO GENERATE PLOT ==========
def generate_expense_plot(data, days=30):
    cutoff = datetime.now() - timedelta(days=days)
    filtered = [x for x in data if x['date'] >= cutoff]

    if not filtered:
        return None

    df = pd.DataFrame(filtered)
    grouped = df.groupby(['date', 'category'])['amount'].sum().unstack().fillna(0)
    
    grouped.plot(kind='bar', stacked=True, figsize=(10, 5))
    plt.title(f'Expenses for Last {days} Days')
    plt.xlabel('Date')
    plt.ylabel('Amount (₹)')
    plt.tight_layout()
    plt.savefig('expense_plot.png')
    plt.close()
    return 'expense_plot.png'

# ========== TELEGRAM HANDLERS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("📆 Last 7 Days", callback_data='7')],
        [InlineKeyboardButton("📅 Last 30 Days", callback_data='30')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Choose the range for expense summary:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    days = int(query.data)
    data = fetch_data_from_sheets()
    path = generate_expense_plot(data, days=days)

    if path:
        await query.message.reply_photo(photo=open(path, 'rb'))
    else:
        await query.message.reply_text("No data available to generate the graph.")

# ========== MAIN BOT APP ==========
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot is running...")
    app.run_polling()
