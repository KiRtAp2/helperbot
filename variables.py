import discord


staff_list = (
    discord.User(id="279712997486755840"),
	discord.User(id="288672403121242112"),
)

prevent_message_deletions = True

def safer_eval(expression, allowed_variables, allowed_variables_local, rvl):
    eval_return = eval(expression, allowed_variables, allowed_variables_local)
    rvl = [eval_return]
    return True
