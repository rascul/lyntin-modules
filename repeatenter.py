from lyntin import exported

last_command = ""

def handle_user_filter(args):
	global last_command
	
	command = args['dataadj']
	send_command = args['dataadj']
	
	if last_command:
		if command == "#cr":
			send_command = last_command
		else:
			last_command = command
	else:
		last_command = command
	
	return send_command

def load():
	exported.hook_register("user_filter_hook", handle_user_filter, place=50)

def unload():
	exported.hook_unregister("user_filter_hook", handle_user_filter)
