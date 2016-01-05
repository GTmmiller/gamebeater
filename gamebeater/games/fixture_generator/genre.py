import sys
import json
import copy
from collections import OrderedDict

base_genre = OrderedDict([
	("model", "games.genre"),
	("pk", ""),
	("fields", OrderedDict([
			("description", "There's no description for this genre yet.")
		])
	)
])	

def main(argv):
	genre_data = []

	# assume that argv[1] is the name of a file to parse
	with open(argv[1]) as console_file:
		for line in console_file:
			new_genre = copy.deepcopy(base_genre)
			new_genre["pk"] = line.strip()
			genre_data.append(new_genre)
	print json.dumps(genre_data, indent=2, separators=(',', ': '))
			

if __name__ == '__main__':
	main(sys.argv)