"""
Keeps you from idling out on wotmud. Automagically resets idle counter
ever time there's input from the user.
"""
__author__ = "Ray Schulz"
__version__ = "2.1"
__date__ = "February 14, 2014"

from lyntin import exported, session

# keep track of how long we've been idle
ticks = dict()

def handle_connect(args):
	# add new session to ticks dict except for the common session
	global ticks
	if args['session'].getName() is not 'common':
		ticks[args['session']] = 0

def handle_disconnect(args):
	# remove disconnected session from ticks dict
	global ticks
	del ticks[args['session']]

def handle_timer(args):
	# tick tock
	global ticks
	
	for session in ticks.keys():
		ticks[session] += 1
		
		if ticks[session] >= 200:
			exported.write_message("You have been idle.", ses=session)
			exported.lyntin_command("#raw", internal=1, session=session)
			ticks[session] = 0

def handle_to_mud(args):
	global ticks
	if args['session'].getName() is not 'common':
		ticks[args['session']] = 0

def load():
	exported.hook_register("connect_hook", handle_connect)
	exported.hook_register("disconnect_hook", handle_disconnect)
	exported.hook_register("timer_hook", handle_timer)
	exported.hook_register("to_mud_hook", handle_to_mud)

def unload():
	exported.hook_unregister("connect_hook", handle_connect)
	exported.hook_unregister("disconnect_hook", handle_disconnect)
	exported.hook_unregister("timer_hook", handle_timer)
	exported.hook_unregister("to_mud_hook", handle_to_mud)
