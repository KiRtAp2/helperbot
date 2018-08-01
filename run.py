import multiprocessing
import discord
import math
import logger
import punisher
import variables
import warnings
from string_splitter import StringSplitter
from datetime import datetime as dt

TOKEN = ""

bot = discord.Client()

allowed_functions = vars(math).copy()
allowed_functions["__builtins__"] = None
allowed_functions["__import__"] = '🖕'

forbidden_expressions = (
    '__class__',
    '__import__',
    '__bases__',
    '__subclasses__',
    'os',
    'system',
    'sys',
    '__name__',
    'import',
    'subprocess',
    'getoutput',
    'rm'
)

punisher.init()
splitter = StringSplitter()

@bot.event
async def on_message(msg):

    if msg.author == bot.user:
        return

    if msg.content.startswith("?"):

        cmd, args, modifiers = splitter.retrieve_command(msg.content, '?')


        if cmd=="math":
            try:
                expression = ' '.join(splitter.last_args_all)

                for expr in forbidden_expressions:
                    if expr in expression:
                        await bot.send_message(msg.channel, "Malicious code blocked. You  will be punished according to the server rules. This event will be logged and staff will be notified.")
                        await punisher.punish(bot, msg.author, "Malicious code")
                        await punisher.log_and_send_staff(bot, msg.author, "Malicious code")
                        return

                try:
                    rvl = [eval(expression, allowed_functions, {})]
                    """p = multiprocessing.Process(target=variables.safer_eval, args=(expression, allowed_functions, {}, rvl))
                    p.start()
                    p.join(100)
                    if p.is_alive():
                        p.terminate()
                        await bot.send_message(msg.channel, "Execution time limit exceeded.")
                    else:"""
                    await bot.send_message(msg.channel, "={val}".format(val=str(rvl[0])))
                except:
                    await bot.send_message(msg.channel, "An error occured.")

            except:
                await bot.send_message(msg.channel, "An error occured")


        if cmd=="lag":
            await bot.send_message(msg.channel, "Received at {t}".format(t=dt.now().strftime("%H:%M:%S")))

        if cmd=="kick":

            user_name = args[0]
            if msg.author not in variables.staff_list:
                await bot.send_message(msg.channel, "Permission denied.")
                logger.info("Non-staff member {user} tried to ?kick {user2}. Permission denied.".format(user=str(msg.author), user2=user_name))
                return

            if user_name in variables.staff_list:
                logger.warning("Staff member requested to be kicked by {user}. Denying".format(user=str(msg.author)))
                await bot.send_message(msg.channel, "Permission denied.")
                return


            try:
                await bot.kick(discord.utils.find(lambda m: str(m)==user_name, msg.channel.server.members))
                logger.info("{user} was successfully kicked by {staff_user}".format(user=user_name, staff_user=str(msg.author)))

            except discord.Forbidden:
                logger.error("Could not kick {user}: Permission denied".format(user=user_name))
            except discord.HTTPException:
                logger.error("Kick on {user} failed: discord.HTTPException raised".format(user=user_name))

            if 'del' in modifiers:
                await bot.delete_message(msg)


        if cmd=="ban":
            user_name = args[0]
            if msg.author not in variables.staff_list:
                await bot.send_message(msg.channel, "Permission denied.")
                logger.info("Non staff member {user} tried to ban {user2}. Permission denied.".format(user=str(msg.author), user2=user_name))
                return

            if user_name in variables.staff_list:
                logger.warning("Staff member requested to be banned by {user}. Denying.".format(user=str(msg.author)))
                await bot.send_message(msg.channel, "Could not ban: Permission denied.")
                return

            try:
                await bot.ban(discord.utils.find(lambda m: str(m)==user_name, msg.channel.server.members), delete_message_days=0)
                logger.info("{user} successfully banned by {staff_user}".format(user=user_name, staff_user=str(msg.author)))

            except discord.Forbidden:
                logger.error("Could not ban {user}: Permission denied".format(user=user_name))

            except discord.HTTPException:
                logger.error("Failed to ban {user}: discord.HTTPException raised.".format(user=user_name))

            if 'del' in modifiers:
                await bot.delete_message(msg)

        if cmd=="warn":
            user_name = args[0]

            if msg.author not in variables.staff_list:
                await bot.send_message(msg.channel, "Permission denied.")
                logger.info("Non staff member {user} tried to warn {user2}. Permission denied.".format(user=str(msg.author), user2=user_name))
                return

            warnings.warn(user_name)
            await bot.send_message(msg.channel, "{user}, you have been warned. Continuing to break the server rules might get you punished. You currently have {warns} warnings.".format(user=user_name, warns=warnings.get_warnings(user_name)))
            logger.info("{user} was warned.".format(user=user_name))
            if 'del' in modifiers:
                await bot.delete_message(msg)

        if cmd=="warns":
            user_name = args[0]

            if str(msg.author)==user_name:
                await bot.send_message(msg.channel, "{user}, you have {warns} warnings.".format(user=user_name, warns=warnings.get_warnings(user_name)))
                return

            else:

                if msg.author not in variables.staff_list:
                    await bot.send_message(msg.channel, "Permission denied.")
                    logger.info("{user} tried to view someone else's warnings".format(user=str(msg.author)))
                    return

                if 'here' in modifiers:
                    await bot.send_message(msg.channel, "{user} has {warns} warnings.".format(user=str(user_name), warns=warnings.get_warnings(user_name)))
                else:
                    await bot.send_message(msg.author, "{user} has {warns} warnings.".format(user=str(user_name), warns=warnings.get_warnings(user_name)))

                if 'del' in modifiers:
                    await bot.delete_message(msg)
        
        if cmd=="debug":
            print(msg.author.id)





@bot.event
async def on_message_delete(message):
    if variables.prevent_message_deletions and (message.author not in variables.staff_list):
        await bot.send_message(message.channel, str(message.author)+" tried to delete a message: "+message.content)




@bot.event
async def on_ready():
    print("Logged in as:")
    print(bot.user)
    print(bot.user.id)



if __name__ == '__main__':
    bot.run(TOKEN)


