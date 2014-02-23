"""
comms logging stuff
"""
__author__ = "Ray Schulz"
__version__ = "0.1"
__date__ = "February 21, 2014"

import time
import datetime

import re

from lyntin import exported
from lyntin.modules import modutils

commo_help = """
commo
"""

sessions = dict()
commands_dict = dict()

def handle_from_mud(args):
	global sessions
	
	if not args['session'] in sessions:
		return
	
	t = datetime.datetime.fromtimestamp(time.time()).strftime('%l:%M')
	f = sessions[args['session']]
	
	m = re.match(r'^((o|\*) HP:\w+ MV:\w+ > |)((\033\[(31|33|36))m(.+) (narrates|chats|bellows|tells you|speaks from the \w+) \'(.+)\'\033\[0m)$', args['data'])
	
	if m:
		f.write("[%s] %s\n" % (t, m.group(3)))
		f.flush()
	else:
		m = re.match(r'^((o|\*) HP:\w+ MV:\w+ > |)(You (narrate|bellow|chat|tell .*) \'.+\')$', args['data'])
		if m:
			f.write("[%s] %s\n" % (t, m.group(3)))
			f.flush()

def commo_cmd(session, args, input):
	if args['action'] == "add":
		if not session in sessions:
			f = open(session.getName() + '-comms', 'w')
			sessions[session] = f
			exported.lyntin_command("#showme Session %s now monitored by comms logger" % session.getName(), True, session)
		else:
			exported.lyntin_command("#showme Session %s already monitored by comms logger" % session.getName(), True, session)
	elif args['action'] == "remove":
		if session in sessions:
			sessions[session].close()
			del sessions[session]
			exported.lyntin_command("#showme Session %s no longer monitored by comms logger" % session.getName(), True, session)
		else:
			exported.lyntin_command("#showme Session %s isn't monitored by comms logger" % session.getName(), True, session)
	elif args['action'] == "":
		if len(sessions):
			exported.lyntin_command("#showme Sessions monitored by comms logger:", True, session)
			for s in sessions:
				exported.lyntin_command("#showme %s" % s.getName(), True, session)
		else:
			exported.lyntin_command("#showme No sessions currently monitored by comms logger", True, session)

commands_dict["commo"] = (commo_cmd, "action=")

def load():
	exported.hook_register("from_mud_hook", handle_from_mud)
	modutils.load_commands(commands_dict)
	exported.add_help("commo.commo", commo_help)

def unload():
	exported.hook_unregister("from_mud_hook", handle_from_mud)
	modutils.unload_commands(commands_dict.keys())

