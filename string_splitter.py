import re

class StringSplitter(object):

    last_cmd = ""
    last_args = []
    last_modifiers = {}
    last_args_all = []

    def get_previous_command(self):
        return (self.last_cmd, self.last_args, self.last_modifiers)

    def get_previous_command_nomod(self):
        return (self.last_cmd, self.last_args_all)

    def retrieve_command(self, cmd: str,
                         start_character: str,
                         modifier_pattern: str = r'^-(\S)+$'
                         ):
        """Returns None if not a command, otherwise splits the command into three parts"""
        if not cmd.startswith(start_character):
            return None

        cmds = cmd[1::]
        args = cmds.split(' ')
        cmd = args[0]
        args = args[1::]
        modifiers = {}

        self.last_cmd = cmd
        self.last_args_all = list(args)
        for a in list(args):
            if re.match(modifier_pattern, a):
                if '=' in a:
                    k, v = a.split('=')
                    modifiers[k[1::]]=v
                else:
                    modifiers[a[1::]]=None
                args.remove(a)

        self.last_args = args
        self.last_modifiers = modifiers

        return (cmd, args, modifiers)


