"""
make backslash (\) a shortcut for #raw
so '\' will send '#raw ' and '\where' will send '#raw where'
"""
__author__ = "Ray Schulz"
__version__ = "1.0"
__date__ = "February 13, 2014"

import re
from lyntin import exported

def handle_user_filter(args):
	command = args['dataadj']
	
	if command[0] == '\\':
		return re.sub("^\\\\(.*)$", "#raw \\1", command)
	else:
		return command

def load():
	exported.hook_register("user_filter_hook", handle_user_filter)

def unload():
	exported.hook_unregister("user_filter_hook", handle_user_filter)
