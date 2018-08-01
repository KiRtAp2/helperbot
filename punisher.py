import json

import logger
import variables

rules = {}

async def punish(bot, user, reason):
    try:
        if rules[reason] == "kick":
            await bot.kick(user)
        if rules[reason] == "ban":
            await bot.ban(user, delete_message_days=0)
        if rules[reason] == "mute":
            if not user.voice.mute:
                await bot.server_voice_state(user, mute=True)
        if rules[reason] == "deafen":
            if not user.voice.deaf:
                await bot.server_voice_state(user, deafen=True)
        return 0
    except:
        return -1

def init():
    global rules
    file = open("punishments.json")
    rules = json.load(file)
    file.close()

async def log_and_send_staff(bot, user, reason):
    for staff in variables.staff_list:
        await bot.send_message(staff, "{user} was punished: {punishment} for {reason}".format(user=str(user), punishment=rules[reason], reason=reason))
    logger.info("{user} was punished: {punishment} for {reason}".format(user=str(user), punishment=rules[reason], reason=reason))