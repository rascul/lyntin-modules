"""
Keeps you from idling out on wotmud. Automagically resets idle counter
ever time there's input from the user.
"""
__author__ = "Ray Schulz"
__version__ = "1.0"
__date__ = "February 13, 2014"

from lyntin import exported

# keep track of how long we've been idle
idle_ticks = 0

def handle_timer(args):
	global idle_ticks
	
	idle_ticks += 1
	
	if idle_ticks >= 200:
		exported.write_message("You have been idle.", ses=exported.get_current_session())
		
		# send a carraige return, but with #raw instead of #cr so it doen't
		# conflict with repeatenter
		exported.lyntin_command("#raw", internal=1, session=exported.get_current_session())
		
		idle_ticks = 0

def handle_from_user(args):
	global idle_ticks
	
	idle_ticks = 0

def load():
	exported.hook_register("timer_hook", handle_timer)
	exported.hook_register("from_user_hook", handle_from_user)

def unload():
	exported.hook_unregister("timer_hook", handle_timer)
	exported.hook_unregister("from_user_hook", handle_from_user)
