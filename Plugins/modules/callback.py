from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .. import JN
from config import *
from pyrogram import filters,Client
import re
from pyrogram.errors import UserNotParticipant
from ..database import collection, add_refer_balance, add_default_balance
from pyrogram.enums import ChatMemberStatus
from Plugins.modules.withdraw import decrease_balance
# Callback handler
@JN.on_callback_query()
async def callback_all(client, query: CallbackQuery):
    # print(query.data)
    if query.data.startswith("approve"):
        print("hii")
        datas = query.data.split("_")
        user_id = int(datas[1])
        amount = float(datas[2])
        upi_id = datas[-1]
    
        print("Approve action", user_id, amount, upi_id)
    
        await JN.send_message(user_id,
        f"Your withdrawal request for INR {amount} has been approved."
    )
        decrease_balance(user_id, amount)
        await query.answer("Withdrawal approved.")

    if query.data.startswith("reject"):
        datas = query.data.split("_")
        user_id = int(datas[1])
        amount = float(datas[2])
        upi_id = datas[-1]
    
        print("Reject action", user_id, amount, upi_id)
        collection.update_one({'user_id': user_id}, {'$inc': {'balance': amount}})
        await JN.send_message(user_id,f"Your withdrawal request for INR {amount} has been rejected. The amount has been refunded to your balance."
    )
        await query.answer("Withdrawal rejected.")
    
    
    if query.data.startswith("joined"):
        datas=query.data.split("_")
        user_id=int(datas[1].replace("{","").replace("}", ""))
        referred_by=datas[-1]

        print("line 56", user_id, referred_by)
        try:
            user = await client.get_chat_member(UPDATE_CHNL, user_id)
            support = await client.get_chat_member(SUPPORT_GRP, user_id)
            # print(user)
            if user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.OWNER,ChatMemberStatus.ADMINISTRATOR] and support.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.OWNER,ChatMemberStatus.ADMINISTRATOR]:
                add_refer_balance(user_id=referred_by, refer_in=REFER_BONUS)
                add_default_balance(user_id=user_id)
                await client.send_message(user_id, f"Congratulations! You've received {NEW_USER_BONUS}₹ as a new user bonus.")
                await client.send_message(referred_by, f"Congratulations! You've received {REFER_BONUS}₹ for referring a new user.")
                await JN.send_message(log_channel, text=f"🦋 #bonus 🦋,\n\n**ID** : {user_id}\n**Name**: {query.from_user.first_name}\n**Referred by**: {referred_by}\n**Bonuses awarded**: {NEW_USER_BONUS}₹ to new user, {REFER_BONUS}₹ to referrer")
                await query.answer("You have successfully joined the channels and received your bonus! 🎉")
            else:
                await query.answer("You need to join both the Update Channel and Support Group to receive the bonuses. hi", show_alert=True)
        except UserNotParticipant:
            await query.answer("You need to join both the Update Channel and Support Group to receive the bonuses. ❌", show_alert=True)