from .. import JN
from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from ..database import collection
from config import OWNER_ID as owner_id, main_button
import asyncio

def decrease_balance(user_id, amount):
    collection.update_one({'user_id': user_id}, {'$inc': {'balance': -amount}})

@JN.on_message((filters.regex("⚡️ ᴡɪᴛʜᴅʀᴀᴡᴀʟ ⚡️") | filters.command("withdrawal")) & filters.private)
async def withdrawal(bot, message):
    document = collection.find_one({"user_id": message.from_user.id})
    balance = document.get("balance")

    msg1 = await JN.ask(message.from_user.id, "How much money do you want to withdraw?", reply_markup=main_button)
    try:
        amount = float(msg1.text)
    except ValueError:
        await message.reply_text("Invalid amount. Please enter a valid number.", reply_markup=main_button)
        return

    if amount > balance:
        await message.reply_text("Insufficient balance. Please enter a valid amount.", reply_markup=main_button)
        return

    msg2 = await JN.ask(message.from_user.id, "Please provide your UPI ID.", reply_markup=main_button)
    upi_id = msg2.text

    # Decrease the user's balance
    # decrease_balance(message.from_user.id, amount)

    # Send details to the owner for approval
    await bot.send_message(
        owner_id,
        f"New withdrawal request:\n\n"
        f"User: {message.from_user.mention}\n"
        f"Amount: {amount}\n"
        f"UPI ID: {upi_id}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Approve", callback_data=f"approve_{message.from_user.id}_{amount}_{upi_id}")],
            [InlineKeyboardButton("Reject", callback_data=f"reject_{message.from_user.id}_{amount}_{upi_id}")]
        ])
    )

    await message.reply_text("Your withdrawal request has been sent for approval.", reply_markup=main_button)

