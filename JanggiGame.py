# Author:           Chi Hang Leung
# Date:             03/09/2021
# Description:      A complete Janggi game that can be played on the terminal.


class JanggiGame:
	"""A class that represent the Janggi game board.
	Includes methods to move a move on the Janggi board and print out the Janggi board on the terminal."""

	def __init__(self):
		"""Instantiated the Janggi Game Board. Takes no parameters and initiate all game pieces for each player."""

		# Board size: 10 rows and 9 columns
		self._rows = 10
		self._columns = 9

		# Representing the Janggi board as a dictionary:
			# Key:      the position of the game piece as a 2-tuple [e.g. (0, 0) for A1].
			# Value:    the object of the game piece
		self._board = {(i, j): None for i in range(self._rows) for j in range(self._columns)}

		# Create a dictionary to represent the players and the game pieces thay currently hold.
				# Key: the player, either "RED" or "BLUE".
				# Value: a list that contains all the game pieces hold by each player.

		# Representing all games pieces that each player holds as a dictionary:
			# Key:      the player (either BLUE or RED)
			# Value:    the object of the game piece
		# Create all game pieces for each player store in the dictionary.
		self._players = {player: [General(player, 0),
		                          Guard(player, 0), Guard(player, 1),
		                          Horse(player, 0), Horse(player, 1),
		                          Elephant(player, 0), Elephant(player, 1),
		                          Chariot(player, 0), Chariot(player, 1),
		                          Cannon(player, 0), Cannon(player, 1),
		                          Soldier(player, 0), Soldier(player, 1),
		                          Soldier(player, 2), Soldier(player, 3), Soldier(player, 4)]
		                 for player in ["BLUE", "RED"]}

		# Add each game piece of each player to the board at their corresponding starting positions.
		for player in self._players:
			for game_piece in self._players[player]:
				self._board[game_piece.get_starting_position()] = game_piece

		# Blue always plays first
		self._turn = "BLUE"

		# Game Status started as "UNFINISHED". Game Status can be 'UNFINISHED' or 'RED_WON' or 'BLUE_WON'.
		self._status = "UNFINISHED"

	def get_rows(self):
		"""Returns the number of rows of the game board."""
		return self._rows

	def get_columns(self):
		"""Returns the number of columns of the game board."""
		return self._columns

	def get_board(self):
		"""Returns the entire dictionary representing the game board."""
		return self._board

	def get_players(self):
		"""Return the entire dictionary holding all the game pieces for each player."""
		return self._players

	def get_turn(self):
		"""Returns the player who should be playing at this turn, either "RED" or "BLUE"."""
		return self._turn

	def get_game_state(self):
		"""Returns the current state of the game, which can be either "UNFINISHED", "RED_WON" or "BLUE_WON"."""
		return self._status

	def get_position(self, GamePieceObject):
		"""Takes a game piece object as parameter and returns its position on the board.
		Return None if the game piece has been captured and is no longer on the board."""
		for position in self._board:
			if self._board[position] is GamePieceObject:
				return position
		return None

	def convert_position(self, square):
		"""Takes a position (a string), represented by column (A-I) and rows (1-10), and
		returns the position in a 2-tuple format (i, j),
		where i represents the row (0 - 9) and j represents the column (0 - 8)."""

		# Square must be between 2 - 3 characters in length
		if len(square) > 3 or len(square) <= 1:
			raise InvalidPositionError

		# The first character must be an alphabet
		if not 'A' <= square[0] <= 'I' and not 'a' <= square[0] <= 'i':
			raise InvalidPositionError

		# Only A10 to I10 should have position (square) with 3 characters.
		if len(square) == 3:
			if square[1:] != '10':
				raise InvalidPositionError

		# The second letter much be a digit
		if len(square) == 2 and not '1' <= square[1] <= '9':
			raise InvalidPositionError

		# Convert string position (square) to the 2-tuple format.
		row = int(square[1:]) - 1
		column = ord(square[0].upper()) - 65
		return (row, column)

	def get_opponent(self, player):
		"""Takes the player, either "RED" or "BLUE", of the game as parameter and return his/her opponent."""
		return "RED" if player == "BLUE" else "BLUE"

	def try_move(self, fromPosition, toPosition):
		"""Takes the from and to position as parameters and attempt to make the move. Returns the captured game piece.
		"""

		captured = self._board[toPosition]
		self._board[toPosition] = self._board[fromPosition]
		self._board[fromPosition] = None
		if captured is not None:
			self._players[captured.get_player()].remove(captured)
		return captured

	def restore_move(self, fromPosition, toPosition, captured):
		"""Takes the from and to position and the captured game piece as parameters and
		restore the previously made move. Returns None."""

		self._board[fromPosition] = self._board[toPosition]
		self._board[toPosition] = captured
		if captured is not None:
			self._players[captured.get_player()].append(captured)

	def is_in_check(self, player):
		"""Takes the player, either "RED" or "BLUE", as the parameter, and
		returns True if that player is in check (could be captured on the opposing player's next move).
		Return False otherwise."""

		# Converting all input player as upper case
		player = player.upper()

		# Iterate every legal moves of every game piece held by the opponent and
		# check if there is a move that can capture the player's general.
		checked = False
		for gamePiece in self._players[self.get_opponent(player)]:
			for move in gamePiece.legal_moves(self._board, self.get_position(gamePiece)):
				if self._board[move] == self._players[player][0]:
					checked = True
		return checked

	def is_checkmate(self, player):
		"""Takes the player, either "RED" or "BLUE", as the parameter,
		 and returns True if the player has been checkmated. Returns False otherwise."""

		# If the player is not being in check, then it is not checkmated.
		if not self.is_in_check(player):
			return False

		# Iterate every legal move of every game piece held by the player.
		# The player is not checkmated if there exists a move that can get out of being in check.
		checkmated = True
		i = 0
		while i < len(self._players[player]) and checkmated:
			gamePiece = self._players[player][i]
			i += 1

			legalMoves = list(gamePiece.legal_moves(self._board, self.get_position(gamePiece)))
			j = 0
			while j < len(legalMoves) and checkmated:
				toPosition = legalMoves[j]
				fromPosition = self.get_position(gamePiece)
				j += 1

				# Do not attempt to make the move if the player is passing the turn.
				if toPosition == fromPosition:
					continue

				# Attempts at making the move
				captured = self.try_move(fromPosition, toPosition)

				# Check if the player is still being in check
				if not self.is_in_check(player):
					checkmated = False

				# Restoring the move
				self.restore_move(fromPosition, toPosition, captured)

		return checkmated

	def make_move(self, fromSquare, toSquare):
		"""Takes from and to squares (positions in strings). Return False if the move is illegal.
		Otherwise make the indicated move, remove any captured piece from the player,
		check if the opponent has been checkmate, update the game state, update whose turn it is, and return True."""

		# Check if the game has already been won
		if self._status != "UNFINISHED":
			return False

		# Convert the squares moving from and moving into a 2-tuple format
		try:
			fromPosition = self.convert_position(fromSquare)
			toPosition = self.convert_position(toSquare)
		except InvalidPositionError:
			return False

		# Check if the position moving from contains a game piece
		if self._board[fromPosition] is None:
			return False

		# Check if the square moving from is own by the current player
		if self._board[fromPosition].get_player() != self._turn:
			return False

		# Check if the position moving to is one of the legal moves that can be made by the game piece at fromPosition
		if toPosition not in self._board[fromPosition].legal_moves(self._board, fromPosition):
			return False

		# If the position being moved from and moved to are the same, then it means the player is pass his/her turn.
		if toPosition == fromPosition:

			# However, the player must play if he or she is being in check.
			if self.is_in_check(self._turn):
				return False

		# Making the move
		else:
			# Making the move
			captured = self.try_move(fromPosition, toPosition)

			# Check if the player put himself/herself in check
			if self.is_in_check(self._turn):

				# Restoring the move
				self.restore_move(fromPosition, toPosition, captured)
				return False

		# Determine if the opponent has been checkmated. If so, update the game status.
		if self.is_checkmate(self.get_opponent(self._turn)):
			if self._turn == "RED":
				self._status = "RED_WON"
			else:
				self._status = "BLUE_WON"

		# Switch player's turn
		self._turn = self.get_opponent(self._turn)
		return True

	def print_board(self):
		"""Print the game board, game status, player's turn, and if anyone is being in check on the terminal
		with colored game pieces (Blue or Red)."""

		def cellForPrint(max_spaces, center, left_filler=' ', right_filler=' ', num_cell=1):
			"""Take the maxium number of spaces occupied, the string at the center,
			filler characters on the left and on the right, and the number of repeated cells as parameters.
			Returns a standardized cell (a string) to be printed on the terminal."""
			left = (max_spaces - len(center)) // 2
			right = max_spaces - len(center) - left
			cell = left * left_filler + center + right * right_filler
			return cell * num_cell

		# Each cell should have 13 characters in width and leaving 5 spaces to show the numbering of the rows.
		max_spaces = 13
		row_spaces = 5

		# Define the locations of the fortresses
		fortress_red = [(i, j) for i in range(0, 3) for j in range(3, 6)]
		fortress_blue = [(i, j) for i in range(7, 10) for j in range(3, 6)]
		fortress = fortress_red + fortress_blue

		# Spacer for numbering the rows
		row_spacer = cellForPrint(row_spaces, '')

		# Cells that represent the space where the game piece can go but there is no game piece at the moment.
		empty_space = {"other": cellForPrint(max_spaces, "[ ]", '-', '-'),
		               0: cellForPrint(max_spaces, "[ ]", ' ', '-'),
		               self._columns - 1: cellForPrint(max_spaces, "[ ]", '-', ' ')}

		# Cells that represent the fortress
		empty_space_fortress = {3: cellForPrint(max_spaces, "[ ]", '-', '='),
		                        4: cellForPrint(max_spaces, "[ ]", '=', '='),
		                        5: cellForPrint(max_spaces, "[ ]", '=', '-')}

		# Create rows to space apart the rows where there game pieces can go.
		empty_row = (row_spacer + cellForPrint(max_spaces, "|", num_cell=self._columns) + "\n") * 2
		empty_row_fortress = (row_spacer + cellForPrint(max_spaces, "|", num_cell=self._columns//2-1) +
		                      cellForPrint(max_spaces, "║", num_cell=self._columns//2-1) +
		                      cellForPrint(max_spaces, "|", num_cell=self._columns//2-1) + '\n') * 2

		# Show label for the rows and columns
		print()
		print("ROW  " + cellForPrint(max_spaces, '', num_cell=4) + cellForPrint(max_spaces, "COLUMN", ' ', ' '))

		# Show the column names from A to I
		print(row_spacer, end="")
		for i in range(self._columns):
			print(cellForPrint(max_spaces, chr(i + 65), ' ', ' '), end="")
		print()

		# Print out the entire board
		for i in range(self._rows):

			# Numbering the rows
			print(cellForPrint(row_spaces, str(i + 1)), end="")

			# Print out each game piece if they exist. Otherwise, print empty cells.
			for j in range(self._columns):
				gamePiece = self._board[(i, j)]
				if gamePiece:
					gamePiece.print_name(max_spaces)
				else:
					if j in empty_space:
						print(empty_space[j], end="")
					elif (i, j) in fortress:
						print(empty_space_fortress[j], end="")
					else:
						print(empty_space["other"], end="")

			# Print spacer between rows
			print()
			if i == self._rows - 1:
				continue
			if i < 2 or i > 6:
				print(empty_row_fortress, end="")
			else:
				print(empty_row, end="")

		# Show the status of the game.
		print()
		print("Game state:", self._status)
		if self.is_in_check("BLUE"):
			print("Blue is in check!!!")
		elif self.is_in_check("RED"):
			print("Red is in check!!!")

		if self._status == "UNFINISHED":
			print(f"It is now {self._turn}'s turn!\n")
		print()


class GamePiece:
	"""A class that represent individual game piece."""

	def __init__(self, player, identifier):
		"""Instantiate the game piece."""

		# Player who own the game piece, either RED or BLUE
		self._player = player

		# The identifier for different game pieces of the same type
		self._identifier = identifier

		# Define the game piece's own fortress
		if self._player == "RED":
			fortress_row_start = 0
			fortress_row_end = 3
		else:
			fortress_row_start = 7
			fortress_row_end = 10

		fortress_column_start = 3
		fortress_column_end = 6

		self._fortress = {(i, j) for i in range(fortress_row_start, fortress_row_end)
		                  for j in range(fortress_column_start, fortress_column_end)}

		# Define a set of standard diagonal moves for the game piece.
		self._diagonalMoves = {(1, 4): {(0, 3), (0, 5), (2, 3), (2, 5)},
			                   (0, 3): {(1, 4)},
			                   (0, 5): {(1, 4)},
			                   (2, 3): {(1, 4)},
			                   (2, 5): {(1, 4)},
			                   (8, 4): {(7, 3), (7, 5), (9, 3), (9, 5)},
			                   (7, 3): {(8, 4)},
			                   (7, 5): {(8, 4)},
			                   (9, 3): {(8, 4)},
			                   (9, 5): {(8, 4)}}

	def get_player(self):
		"""Returns the player who own the game piece."""
		return self._player

	def get_identifier(self):
		"""Returns the identifier of the game piece."""
		return self._identifier

	def get_fortress(self):
		"""Return the set with all positions in the player's fortress."""
		return self._fortress

	def get_diagonalMoves(self, position):
		"""Takes a position as parameter and return a standard set of diagonal moves.
		The position parameter must be a position where a diagonal move is possible."""
		return self._diagonalMoves[position]

	def get_starting_position(self):
		"""Returns the starting position of the game piece
		based on what game piece it is, who owns the game piece, and the identifier of the game piece."""
		return self._starting_position[(self._player, self._name, self._identifier)]

	def get_name(self):
		"""Return the name of the game piece."""
		return self._name

	def print_name(self, max_space):
		"""Takes the maximum width as parameter and
		print the name of the game piece with brackets on screen with appropriate spacing and color."""

		if self._player == "RED":
			ANSI_code = 31
		else:
			ANSI_code = 34

		max_space -= 2      # Preserve two spaces for the brackets
		pre_space = (max_space - len(self._name)) // 2
		post_space = max_space - len(self._name) - pre_space
		gamePieceToPrint = '[' + pre_space * ' ' + self._name + post_space * ' ' + ']'
		print(f'\033[{ANSI_code}m' + gamePieceToPrint + f'\033[0m', end="")


class General(GamePiece):
	"""A class that represent the General. Inherited from GamePiece."""

	def __init__(self, player, identifier):
		"""Instantiate the General object."""
		super().__init__(player, identifier)
		self._name = "General"
		self._starting_position = {("RED", "General", 0) : (1, 4),
		                           ("BLUE", "General", 0) : (8, 4)}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the General can play next."""

		legalMoves = set()

		# Add all vertical and horizontal moves
		for i in range(-1, 2):
			for j in range(-1, 2):
				if abs(i + j) == 1:
					legalMoves.add((current_position[0] + i, current_position[1] + j))

		# Add any available diagonal moves
		if current_position in self._diagonalMoves:
			legalMoves = legalMoves.union(self._diagonalMoves[current_position])

		# Remove all moves that are outside of the fortress
		legalMoves = legalMoves.intersection(self._fortress)

		# Remove all moves that are occupied by other game pieces own by the same player
		for move in list(legalMoves):
			if board[move] is not None and board[move].get_player() == self._player:
				legalMoves.remove(move)

		# Add the current position
		legalMoves.add(current_position)
		return legalMoves


class Guard(GamePiece):
	"""A class that represent the Guards. Inherited from GamePiece."""

	def __init__(self, player, identifier):
		"""Instantiate the Guard object."""
		super().__init__(player, identifier)
		self._name = "Guard"
		self._starting_position = {("RED", "Guard", 0)  :   (0, 3),
		                           ("RED", "Guard", 1)  :   (0, 5),
		                           ("BLUE", "Guard", 0) :   (9, 3),
		                           ("BLUE", "Guard", 1) :   (9, 5)}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Guard can play next."""

		# Mimick the movements of the general
		mimic_general = General(self._player, 0)
		legalMoves = mimic_general.legal_moves(board, current_position)
		return legalMoves


class Horse(GamePiece):
	"""A class that represent Horses. Inherited from GamePiece."""

	def __init__(self, player, identifier):
		"""Instantiate the Horse object."""
		super().__init__(player, identifier)
		self._name = "Horse"
		self._starting_position = {("RED", "Horse", 0)  :   (0, 2),
		                           ("RED", "Horse", 1)  :   (0, 7),
		                           ("BLUE", "Horse", 0) :   (9, 2),
		                           ("BLUE", "Horse", 1) :   (9, 7)}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Horse can play next."""

		# Adding the current position
		legalMoves = set()
		legalMoves.add(current_position)

		# First iterate all orthogonal move by 1 space to determine if it is being blocked
		x, y = current_position
		for i in range(-1, 2):
			for j in range(-1, 2):
				if abs(i + j) != 1:
					continue
				if (x + i, y + j) not in board:
					continue
				if board[(x + i, y + j)] is not None:
					continue

				# Then iterate all diagonal move by 1 square and add legal moves to the set.
				for m in range(-1 + i, 2 + i):
					for n in range(-1 + j, 2 + j):
						if abs(m) + abs(n) != 3:
							continue
						if (x + m, y + n) not in board:
							continue
						if board[(x + m, y + n)] is not None and board[(x + m, y + n)].get_player() == self._player:
							continue
						legalMoves.add((x + m, y + n))

		return legalMoves


class Elephant(GamePiece):
	"""A class that represent the Elephants. Inherited from GamePiece."""

	def __init__(self, player, identifier):
		"""Instantiate the Elephant object."""
		super().__init__(player, identifier)
		self._name = "Elephant"
		self._starting_position = {("RED", "Elephant", 0)  :   (0, 1),
		                           ("RED", "Elephant", 1)  :   (0, 6),
		                           ("BLUE", "Elephant", 0) :   (9, 1),
		                           ("BLUE", "Elephant", 1) :   (9, 6)}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Elephant can play next."""

		# Add the current position
		legalMoves = set()
		legalMoves.add(current_position)

		# First iterate all orthogonal move by 1 space and see if it is being blocked
		x, y = current_position
		for i in range(-1, 2):
			for j in range(-1, 2):
				if abs(i + j) != 1:
					continue
				if (x + i, y + j) not in board:
					continue
				if board[(x + i, y + j)] is not None:
					continue

				# Then iterate all diagonal move by 1 square  and see if it is being blocked
				for m in range(-1+i, 2+i):
					for n in range(-1+j, 2+j):
						if abs(m) + abs(n) != 3:
							continue
						if (x + m, y + n) not in board:
							continue
						if board[(x + m, y + n)] is not None:
							continue

						# Iterate one more diagonal move by 1 square and add all legal moves to the set
						for p in range(-1 + m, 2 + m):
							for q in range(-1 + n, 2 + n):
								if abs(p) + abs(q) != 5:
									continue
								if (x + p, y + q) not in board:
									continue
								if board[(x + p, y + q)] is not None and board[
									(x + p, y + q)].get_player() == self._player:
									continue
								legalMoves.add((x + p, y + q))

		return legalMoves


class Chariot(GamePiece):
	"""A class that represent Chariots. Inherited from GamePiece."""

	def __init__(self, player, identifier):
		"""Instantiate the Chariot object."""
		super().__init__(player, identifier)
		self._name = "Chariot"
		self._starting_position = {("RED", "Chariot", 0)  :   (0, 0),
		                           ("RED", "Chariot", 1)  :   (0, 8),
		                           ("BLUE", "Chariot", 0) :   (9, 0),
		                           ("BLUE", "Chariot", 1) :   (9, 8)}

		self._diagonalMovesExtendedRed = {(0, 3): (2, 5),
		                                  (0, 5): (2, 3),
		                                  (2, 3): (0, 5),
		                                  (2, 5): (0, 3)}

		self._diagonalMovesExtendedBlue = {(7, 3): (9, 5),
		                                   (7, 5): (9, 3),
		                                   (9, 3): (7, 5),
		                                   (9, 5): (7, 3)}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Chariot can play next."""

		def orthogonal_check(position, axis, direction):
			"""Function that check in one direction and only in one axis.
			Takes position, axis, and direction as parameters and return a set of legal moves for the chariot."""

			def update_position(position, axis, direction):
				"""Takes the position, axis to be changed, and the direction of movement as parameters.
				Update and return the new position."""
				position_list = list(position)
				position_list[axis] += direction
				return tuple(position_list)

			# Move in the direction in the specified axis.
			moves = set()
			position = update_position(position, axis, direction)
			while position in board:

				# Chariot can move as long as if the square is empty or containing a game piece belongs to the opponent.
				if board[position] is None:
					moves.add(position)
					position =update_position(position, axis, direction)
				elif board[position].get_player() != self._player:
					moves.add(position)
					break
				else:
					break

			return moves

		def check_extended_diagonal(board, position, diagonalMovesExtended, centerPosition):
			"""Takes the board, current position, dictionary of Extended diagonal moves and
			the center position of the fortress as parameters.
			Returns a set of legal diagonal moves for the Chariot."""

			moves = set()
			if position in diagonalMovesExtended and board[centerPosition] is None:
				extendedDiagonalMove = diagonalMovesExtended[position]
				if board[extendedDiagonalMove].get_player() != self._player:
					moves.add(extendedDiagonalMove)
			return moves

		# Add current position
		legalMoves = set()
		legalMoves.add(current_position)

		# Add all orthogonal moves
		for axis in [0, 1]:
			for direction in [-1, 1]:
				legalMoves = legalMoves.union(orthogonal_check(current_position, axis, direction))

		# Add any available diagonal moves
		if current_position in self._diagonalMoves:
			for move in self._diagonalMoves[current_position]:

				# Adding standard diagonal moves
				if board[move] is None or board[move].get_player() != self._player:
					legalMoves.add(move)

			# Adding extended diagonal moves
			legalMoves = legalMoves.union(check_extended_diagonal(board, current_position,
			                                                      self._diagonalMovesExtendedRed, (1, 4)))
			legalMoves = legalMoves.union(check_extended_diagonal(board, current_position,
			                                                      self._diagonalMovesExtendedBlue, (8, 4)))

		return legalMoves


class Cannon(GamePiece):
	"""A class that represent Cannon. Inherited from GamePiece."""

	def __init__(self, player, identifier):
		"""Instantiate the Cannon object."""
		super().__init__(player, identifier)
		self._name = "Cannon"
		self._starting_position = {("RED", "Cannon", 0)  :   (2, 1),
		                           ("RED", "Cannon", 1)  :   (2, 7),
		                           ("BLUE", "Cannon", 0) :   (7, 1),
		                           ("BLUE", "Cannon", 1) :   (7, 7)}

		self._diagonalMovesExtendedRed = {(0, 3): (2, 5),
		                                  (0, 5): (2, 3),
		                                  (2, 3): (0, 5),
		                                  (2, 5): (0, 3)}

		self._diagonalMovesExtendedBlue = {(7, 3): (9, 5),
		                                   (7, 5): (9, 3),
		                                   (9, 3): (7, 5),
		                                   (9, 5): (7, 3)}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Cannon can play next."""

		def jump_over_check(position, axis, direction):
			"""Function that check in one direction in one axis and determine what moves are valid.
			 Takes the position of the cannon, axis to be checked, and direction as parameters.
			 Returns a set of legal moves for the cannon."""

			def update_position(position, axis, direction):
				"""Takes the position, axis to be changed, and the direction of movement as parameters.
				Update and return the new position."""

				position_list = list(position)
				position_list[axis] += direction
				return tuple(position_list)

			# Move toward the direction at the specified axis one square at a time.
			moves = set()
			position = update_position(position, axis, direction)
			jumped = False
			while position in board:

				# Cannon cannot jump over or capture another cannon
				if board[position] is not None and board[position].get_name() == "Cannon":
					break

				# If the Cannon has already jumped, then all empty squares or game pieces of the opponent's are legal
				if jumped:
					if board[position] is None:
						moves.add(position)
					elif board[position].get_player() != self._player:
						moves.add(position)
						break
					else:
						break

				# Keep track of if Cannon has jumped.
				elif board[position] is not None:
					jumped = True

				position = update_position(position, axis, direction)

			return moves

		def check_diagonal(board, position, diagonalMovesExtended, centerPosition):
			"""Takes the board, position, the dictionary of extended diagonal moves,
			 and the center position of the fortress as parameters.
			 Return a set of legal diagonal moves for the Cannon."""
			moves = set()
			if position in diagonalMovesExtended:
				extendedDiagonalMove = diagonalMovesExtended[position]
				if board[centerPosition] is not None and board[centerPosition].get_name() != "Cannon":
					if board[extendedDiagonalMove] is None:
						moves.add(extendedDiagonalMove)
					elif board[extendedDiagonalMove].get_player() != self._player and \
							board[extendedDiagonalMove].get_name() != "Cannon":
						moves.add(extendedDiagonalMove)
			return moves

		# Adding the current position
		legalMoves = set()
		legalMoves.add(current_position)

		# Adding all orthogonal moves
		for axis in [0, 1]:
			for direction in [-1, 1]:
				legalMoves = legalMoves.union(jump_over_check(current_position, axis, direction))

		# Adding all available diagonal moves
		legalMoves = legalMoves.union(check_diagonal(board, current_position, self._diagonalMovesExtendedRed, (1, 4)))
		legalMoves = legalMoves.union(check_diagonal(board, current_position, self._diagonalMovesExtendedBlue, (8, 4)))

		return legalMoves


class Soldier(GamePiece):
	"""A class that represent Soldier. Inherited from GamePiece"""

	def __init__(self, player, identifier):
		"""Instantiate the Soldier object."""
		super().__init__(player, identifier)
		self._name = "Soldier"
		self._starting_position = {("RED", "Soldier", 0)    :   (3, 0),
		                           ("RED", "Soldier", 1)    :   (3, 2),
		                           ("RED", "Soldier", 2)    :   (3, 4),
		                           ("RED", "Soldier", 3)    :   (3, 6),
		                           ("RED", "Soldier", 4)    :   (3, 8),
		                           ("BLUE", "Soldier", 0)   :   (6, 0),
		                           ("BLUE", "Soldier", 1)   :   (6, 2),
		                           ("BLUE", "Soldier", 2)   :   (6, 4),
		                           ("BLUE", "Soldier", 3)   :   (6, 6),
		                           ("BLUE", "Soldier", 4)   :   (6, 8)}

		self._diagonalMovesExtended = {(2, 3): {(1, 4)},
		                               (2, 5): {(1, 4)},
			                           (1, 4): {(0, 3), (0, 5)},
			                           (7, 3): {(8, 4)},
			                           (7, 5): {(8, 4)},
			                           (8, 4): {(9, 3), (9, 5)}}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Soldier can play next."""

		def update_position(position, axis, direction):
			"""Takes the position, axis and the direction of movement as parameters.
			Returns the the new position."""

			position_list = list(position)
			position_list[axis] += direction
			return tuple(position_list)

		# Adding the current position
		legalMoves = set()
		legalMoves.add(current_position)

		# Red soldiers can only move downward and Blue soldiers can only move upward.
		if self._player == "RED":
			direction = 1
		else:
			direction = -1

		# Adding all orthogonal moves
		orthogonal_moves = {update_position(current_position, 0, direction),
							update_position(current_position, 1, -1),
		                    update_position(current_position, 1, 1)}

		# Removing any moves that not in-bound and occupied by other game pieces owned by the player
		for move in orthogonal_moves:
			if move in board and (board[move] is None or board[move].get_player() != self._player):
				legalMoves.add(move)

		# Adding all extended diagonal moves
		if current_position in self._diagonalMovesExtended:
			extendedDiagonalMove = self._diagonalMovesExtended[current_position]
			for move in extendedDiagonalMove:
				if board[move] is None or board[move].get_player() != self._player:
					legalMoves.add(move)

		return legalMoves


class InvalidPositionError(Exception):
	"""Raised when the input position of the board is invalid."""
	pass

# Try me!!!
# def game_console():
# 	"""Game console to activate the game to be played."""
# 	game = JanggiGame()
#
# 	# Repeat as long as the game is not finished
# 	while game.get_game_state() == "UNFINISHED":
# 		game.print_board()
# 		validInput = False
#
# 		# Repeat if the user input is invalid
# 		while not validInput:
# 			fromSquare = input("Where are you moving from? ")
# 			toSquare = input("Where are youe7 moving to? ")
# 			if game.make_move(fromSquare, toSquare):
# 				validInput = True
# 			else:
# 				print("The move is invalid. Try again!")
# 				print()
#
# if __name__ == "__main__":
# 	game_console()