import sys
import json
import copy
from collections import OrderedDict

base_console = OrderedDict([
	("model", "games.console"),
	("pk", ""),
	("fields", OrderedDict([
			("emulatable", False),
			("generation", 8)
		])
	)
])

script_states = {
	'starting': 'generation',
	'generation': 'console',
	'console': 'generation'
}

def main(argv):
	current_state = 'starting'
	current_generation = 0
	console_data = []

	# assume that argv[1] is the name of a file to parse
	with open(argv[1]) as console_file:
		for line in console_file:
			if line.strip() == '*':
				current_state = script_states[current_state]
			elif current_state == 'generation':
				current_generation = int(line.strip())
			elif current_state == 'console':
				new_console = copy.deepcopy(base_console)
				new_console["pk"] = line.strip()
				new_console["fields"]["generation"] = current_generation
				console_data.append(new_console)
			else:
				print "Error in state change"
	print json.dumps(console_data, indent=2, separators=(',', ': '))
			

if __name__ == '__main__':
	main(sys.argv)