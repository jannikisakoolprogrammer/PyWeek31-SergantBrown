import sys
import os
import random

def main():
	if sys.argv[1] and sys.argv[2] and sys.argv[3]:
	
		tiles = ("#", " ", " ", " ")
		rows = int(sys.argv[1])
		cols = int(sys.argv[2])
		filename = sys.argv[3]
		
		tilemap = ""
		for r in range(rows):
			for c in range(cols):
				if r == 0 or r == (rows - 1) or c == 0 or c == (cols - 1):
					tilemap += "#"
				else:
					tilemap += random.choice(tiles)
			tilemap += "\n"

		# Save.
		filehandle = open(filename, "w")
		filehandle.write(tilemap)
		filehandle.close()

main()