from lyntin import exported

# this holds the lyntin tick value of the last time i executed a lyntin command
lyntin_tick = 0

# keep track if we're idling longer than 60 seconds
idle_flag = 0

# tie current tick
current_tick = 0

def handle_timer(args):
	global idle_flag, lyntin_tick, current_tick
	
	current_tick = args["tick"]
	delta = current_tick - lyntin_tick
	if delta > 60:
		idle_flag = 1
		#exported.lyntin_command("#showme idle for %d seconds" % delta, internal=1)

def handle_from_user(args):
	global idle_flag, lyntin_tick, current_tick
	
	if idle_flag == 1:
		#exported.lyntin_command("#showme stopping idle timer", internal=1)
		idle_flag = 0
	
	lyntin_tick = current_tick

def load():
	exported.hook_register("timer_hook", handle_timer)
	exported.hook_register("from_user_hook", handle_from_user)

def unload():
	exported.hook_unregister("timer_hook", handle_timer)
	exported.hook_unregister("from_user_hook", handle_from_user)
