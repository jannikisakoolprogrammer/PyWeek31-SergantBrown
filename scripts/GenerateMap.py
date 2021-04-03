#    Sergant Brown - LaserTag Traning - A game written using Python and Pygame for PyWeek #31
#    Copyright (C) 2021  Master47
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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