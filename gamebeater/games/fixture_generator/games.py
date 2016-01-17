import sys
import json

def main(argv):
	game_data = []

	# assume that argv[1] is the name of a file to parse
	with open(argv[1]) as console_file:
		game_data = json.load(console_file)
	
	for index, game in enumerate(game_data):
		game["pk"] = index + 1
		del(game["fields"]["goal"])
	print json.dumps(game_data, indent=2, separators=(',', ': '))

if __name__ == '__main__':
	main(sys.argv)
