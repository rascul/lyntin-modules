"""
grabs room names, descriptions and exits from mud, sets some variables
"""
__author__ = "Ray Schulz"
__version__ = "2.0"
__date__ = "February 15, 2014"

import re

from lyntin import exported

sessions = dict()

def handle_connect(args):
	# add new session to sessions dict except for the common session
	global sessions
	if args['session'].getName() is not 'common':
		# initialize some empty values
		s = dict()
		s['matched_room'] = False
		s['room_name'] = ""
		s['room_desc'] = ""
		s['room_exit'] = ""
		sessions[args['session']] = s

def handle_disconnect(args):
	# remove disconnected session from sessions dict
	global sessions
	if args['session'] in sessions:
		del sessions[args['session']]

def handle_from_mud(args):
	global sessions
	
	if not args['session'] in sessions:
		return
	
	if not sessions[args['session']]['matched_room']:
		if "speaks from the" not in args['data']:
			# let's not waste time on this regex if we're not looking for room name
			m = re.match(r'((o|\*) HP:\w+ MV:\w+ > |)\033\[36m(.*)\033\[0m$', args['data'])
			
			if m:
				# matched room name
				sessions[args['session']]['matched_room'] = True
				exported.lyntin_command("#var {room_name} {%s} quiet=true" % m.group(3), internal=1, session=args['session'])
				sessions[args['session']]['room_name'] = m.group(3)
				sessions[args['session']]['room_desc'] = ""
				sessions[args['session']]['room_exit'] = ""
	else:
		# now we should be looking for exits, anything before that is room desc
		m = re.match('^\\[ obvious exits:(.*)\\]$', args['data'])
		if m:
			# got the exit line
			sessions[args['session']]['room_exit'] = m.group(1).strip()
			sessions[args['session']]['room_desc'] = sessions[args['session']]['room_desc'].rstrip('\n')
			exported.lyntin_command("#var {room_desc} {%s} quiet=true" % sessions[args['session']]['room_desc'], internal=1, session=args['session'])
			exported.lyntin_command("#var {room_exits} {%s} quiet=true" % m.group(1).strip(), internal=1, session=args['session'])
			sessions[args['session']]['matched_room'] = False
		else:
			# it's a desc line
			sessions[args['session']]['room_desc'] += args['data']

def load():
	exported.hook_register("connect_hook", handle_connect)
	exported.hook_register("disconnect_hook", handle_disconnect)
	exported.hook_register("from_mud_hook", handle_from_mud)

def unload():
	exported.hook_unregister("connect_hook", handle_connect)
	exported.hook_unregister("disconnect_hook", handle_disconnect)
	exported.hook_unregister("from_mud_hook", handle_from_mud)
