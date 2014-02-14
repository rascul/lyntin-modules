"""
This is to enable functionality to repeat last command simply by hitting enter.
It uses #cr so you can't use that anymore normally, use #raw instead to send
a carraige return.
"""
__author__ = "Ray Schulz"
__version__ = "1.0"
__date__ = "February 13, 2014"

from lyntin import exported

# this holds the last command that the user entered
last_command = ""

def handle_user_filter(args):
	global last_command
	
	send_command = args['dataadj']
	
	if not args['internal']:
		if last_command:
			if args['dataadj'] == "#cr":
				send_command = last_command
			else:
				last_command = args['dataadj']
		else:
			last_command = args['dataadj']
		return send_command
	
	return args['dataadj']

def load():
	exported.hook_register("user_filter_hook", handle_user_filter)

def unload():
	exported.hook_unregister("user_filter_hook", handle_user_filter)
