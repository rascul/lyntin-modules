"""
grabs room names, descriptions and exits from mud, sets some variables
"""
__author__ = "Ray Schulz"
__version__ = "1.0"
__date__ = "February 13, 2014"

import re

from lyntin import exported

matched_room = False

room_name = ""
room_desc = ""
room_exit = ""

def handle_from_mud(args):
	global room_name, room_desc, room_exit, matched_room
	
	if not matched_room:
		if "speaks from the" not in args['data']:
			# let's not waste time on this regex if we're not looking for room name
			m = re.match(r'((o|\*) HP:\w+ MV:\w+ > |)\033\[36m(.*)\033\[0m$', args['data'])
			
			if m:
				# matched room name
				matched_room = True
				exported.lyntin_command("#var {room_name} {%s} quiet=true" % m.group(3), internal=1)
				room_name = m.group(3)
				room_desc = ""
				room_exit = ""
	else:
		# now we should be looking for exits, anything before that is room desc
		m = re.match('^\\[ obvious exits:(.*)\\]$', args['data'])
		if m:
			# got the exit line
			room_exit = m.group(1).strip()
			room_desc = room_desc.rstrip('\n')
			exported.lyntin_command("#var {room_desc} {%s} quiet=true" % room_desc, internal=1)
			exported.lyntin_command("#var {room_exits} {%s} quiet=true" % m.group(1).strip(), internal=1)
			matched_room = False
		else:
			# it's a desc line
			room_desc += args['data']

def load():
	exported.hook_register("from_mud_hook", handle_from_mud)

def unload():
	exported.hook_unregister("from_mud_hook", handle_from_mud)
