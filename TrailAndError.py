# Print color string
def color(player, piece):

	if player == "Red":
		ANSI_code = 31
	elif player == "Blue":
		ANSI_code = 34
	else:
		ANSI_code = 0

	return f'\033[{ANSI_code}m' + piece + f'\033[0m'

# print(color("Blue", "General"))


# Print chinese characters
chinese_pieces = ("漢楚 士 馬 象 車 包 兵 卒")
print(color("Blue", chinese_pieces))
print(color("Red", chinese_pieces))

