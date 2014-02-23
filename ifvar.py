"""
#ifvar command, like #if except the only test it does is to check if
a variable exists in the current session
"""
__author__ = "Ray Schulz"
__version__ = "1.0"
__date__ = "February 16, 2014"

from lyntin import exported
from lyntin.modules import modutils

ifvar_help = """
Allows you to test for the existence of a variable set with #variable. If the
variable exists than the action will be performed, otherwise the elseaction
(if there is one) will be performed.

example:
  #ifvar {room_name} {#showme You are at: $room_name}
  #ifvar {leader} {#showme $leader is in charge} {#showme You're on your own}
"""

commands_dict = dict()

def ifvar_cmd(session, args, input):
	if args['variable'] in session._vars.keys():
		exported.lyntin_command(args['action'], 1, session)
	elif args['elseaction']:
		exported.lyntin_command(args['elseaction'], 1, session)

commands_dict["ifvar"] = (ifvar_cmd, "variable action elseaction=")

def load():
	modutils.load_commands(commands_dict)
	exported.add_help("ifvar", ifvar_help)

def unload():
	modutils.unload_commands(commands_dict.keys())
