def main():
	coordinate_previously_attacked_x = 0
	coordinate_previously_attacked_y = 0

	for i in range(0,201):
		if (coordinate_previously_attacked_x == 0 and coordinate_previously_attacked_y == 0): #starts search from 2,1
			coord_x = 2
			coord_y = 1
			coordinate_previously_attacked_x = coord_x
			coordinate_previously_attacked_y = coord_y
			print (coord_x,coord_y)
		elif (coordinate_previously_attacked_x == 9 and coordinate_previously_attacked_y == 10): #if checkerboard pattern reaches end of board, starts filling unsearched cells
			coord_x = 1
			coord_y = 1
			coordinate_previously_attacked_x = coord_x
			coordinate_previously_attacked_y = coord_y
			print (coord_x,coord_y)
		elif coordinate_previously_attacked_x+2 <= 10:
			coord_x = coordinate_previously_attacked_x+2
			coord_y = coordinate_previously_attacked_y
			coordinate_previously_attacked_x = coord_x
			coordinate_previously_attacked_y = coord_y
			print (coord_x,coord_y)
		elif coordinate_previously_attacked_x+2 > 10:
			if (coordinate_previously_attacked_x%2==0):
				coord_x = 1
			else:
				coord_x = 2
			coord_y = coordinate_previously_attacked_y+1
			coordinate_previously_attacked_x = coord_x
			coordinate_previously_attacked_y = coord_y
			print (coord_x,coord_y)

if __name__ == '__main__':
	main()
