class JanggiGame:
	"""A class that represent the Janggi game board"""

	def __init__(self):
		"""Initiated the Janggi Game Board"""
		# --------------------------------------------------------------------------------------------------------------
		# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
		#
		# 1. Initializing the board
		#    The board will be setup as a dictionary where the key is represented as a 2-tuple (x, y),
		#    where x represents the row and y represents the column.
		# --------------------------------------------------------------------------------------------------------------

		# Set board size: 10 rows and 9 columns
		self._rows = 10
		self._columns = 9

		# Creating an empty dictionary to represent the board
		# Set up the board
			# Go though each row and column of the board
				# Add each position to the board
					# Key: the position as a 2-tuple (e.g. (0, 0) )
					# Value: None
		self._board = {(i, j): None for i in range(self._rows) for j in range(self._columns)}

		# --------------------------------------------------------------------------------------------------------------
		# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
		#
		# 2. Determining how to represent pieces at a given location on the board.
		#    A location on the board will be represented as a 2-tuple (x, y) as stored in the board as a dictionary.
		#    The value of the dictionary holds the object of the game piece, such as the General object.
		#    If the position has no game piece, then the value is None
		# --------------------------------------------------------------------------------------------------------------

		# Create a dictionary to represent the players and the game pieces thay currently hold.
				# Key: the player, either "RED" or "BLUE".
				# Value: a list that contains all the game pieces hold by each player.

		self._players = {player: [General(player, 0),
		                          Guard(player, 0), Guard(player, 1),
		                          Horse(player, 0), Horse(player, 1),
		                          Elephant(player, 0), Elephant(player, 1),
		                          Chariot(player, 0), Chariot(player, 1),
		                          Cannon(player, 0), Cannon(player, 1),
		                          Soldier(player, 0), Soldier(player, 1),
		                          Soldier(player, 2), Soldier(player, 3), Soldier(player, 4)]
		                 for player in ["BLUE", "RED"]}

		# For player RED and BLUE, creating the objects for all game pieces.
			# For each game piece of each player
				# Add the game piece to the board at their corresponding starting positions.
		for player in self._players:
			for game_piece in self._players[player]:
				self._board[game_piece.get_starting_position()] = game_piece


		# Set player's Turn: Blue plays first
		self._turn = "BLUE"

		# Set Game Status as "UNFINISHED". Game Status can be 'UNFINISHED' or 'RED_WON' or 'BLUE_WON'.
		self._status = "UNFINISHED"

	def get_rows(self):
		"""Return the number of rows of the game board."""
		return self._rows

	def get_columns(self):
		"""Return the number of columns of the game board."""
		return self._columns

	def get_board(self):
		"""Return the current game board as an dictionary."""
		return self._board

	def get_players(self):
		"""Return the dictionary for the current players, which holds what game pieces they currently hold."""
		return self._players

	def get_game_state(self):
		"""Return the current state of the game, which can be "UNFINISHED" or "RED_WON" or "BLUE_WON"."""
		return self._status

	def get_position(self, GamePieceObj):
		"""Given a game piece object, return the current position on the board.
		Return None if the game piece is no longer on the board."""

		for position in self._board:
			if self._board[position] is GamePieceObj:
				return position
		return None

	def convert_position_to_tuple(self, Square):
		"""Convert a position (a string) entered by the player to the tuple format. e.g. "A1" to (0, 0)"""

		if len(Square) > 3 or len(Square) <= 1:
			raise InvalidPositionError

		if not 'A' <= Square[0] <= 'I' and not 'a' <= Square[0] <= 'i':
			raise InvalidPositionError

		if not '0' <= Square[1] <= '9':
			raise InvalidPositionError

		if len(Square) == 3:
			if Square[1:] != '10':
				raise InvalidPositionError

		row = int(Square[1:]) - 1
		column = ord(Square[0].upper()) - 65

		return (row, column)

	def convert_position_to_string(self, Square):
		"""Convert a position in a 2-tuple format to the string format. e.g. (0, 0) to "A1" """

		row, column = Square
		return chr(column + 65) + str(row + 1)

	def switch_turn(self, player):
		"""Alternate the current turn of the player.
		If the player is RED, then it will return BLUE.
		If the player is BLUE, then it will return RED."""
		# --------------------------------------------------------------------------------------------------------------
		# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
		# 5. Determining how to track which player's turn it is to play right now.
		#    At the end of make_move method, the game will continue if no one has won yet.
		#    The make_move will set the current player's turn to the opponent by calling the switch_turn method.
		# --------------------------------------------------------------------------------------------------------------
		if player == "BLUE":
			return "RED"
		elif player == "RED":
			return "BLUE"

	def is_in_check(self, player, fromPosition, toPosition):
		"""Takes player, either 'RED' or 'BLUE", and the move about to make (toPosition) as parameters, and
		returns True if that player is in check and return False otherwise."""
		# Make the move and save the position and object of the game piece if it is being captured.
		# Go though all game pieces held by the opponent
			# Extract all possible positions and determine if any of them equal to the position of the General.
				# Return True if there is at least one move that can capture the general.
				# Return False if there is no possible moves that can capture the general.
		# Reverse making the move
		pass

	def is_checkmate(self, opponent):
		"""Takes the opponent as the parameter and determine if his/she has been checkmate."""
		# --------------------------------------------------------------------------------------------------------------
		# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
		# 6. Determining how to detect the checkmate scenario.
		#    Go though all game pieces held by the opponent and determine all legal moves.
		#    If there is no legal moves that the opponent can make to get out of being in check,
		#    then the opponent has been checkmated.
		# --------------------------------------------------------------------------------------------------------------
		pass

	def make_move(self, fromPosition, toPosition):
		"""Takes two strings that represent the squares to move from and the square to move to.
		return False if the move is illegal. Otherwise make the indicated move, remove any captured piece,
		update the game state, update whose turn it is, and return True."""

		# Check if the game has already been won

		# If the square being moved from and moved to are the same, then it means the player is pass his/her turn.

		# Convert the squares moving from and moving to a 2-tuple

		# Check if the square moving from contains a game piece

		# Check if the square moving from is own by the current player

		# --------------------------------------------------------------------------------------------------------------
		# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
		# 3. Determining how to validate a given move according to the rules for each piece,
		#        turn taking and other game rules.
		#    Each game piece is inheriting the GamePiece class and have a their own legal_moves method,
		#    which takes the board and current position as a parameter and
		#    determine what positions are legal moves for that piece.
		#    legal_moves method will be called, via duck typing, by JanggiGame.make_move
		#    to ensure the toPosition is one of the legal moves that the piece can perform.
		# --------------------------------------------------------------------------------------------------------------

		# Check if the square moving to is one of the legal moves that can be made by the game piece at fromPosition

		# Check if the move puts the player's own general in check

		# --------------------------------------------------------------------------------------------------------------
		# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
		# 4. Modifying the board state after each move.
		#    If the opponent have a game piece at the toPosition, then it will be removed from the opponent's inventory.
		#    First replace the game piece object in the toPosition, which will replace any game piece at toPosition.
		#    Then put the value None at the fromPosition.
		#    Check if the opponent has been checkmated.
		#    If so, then the game is over and status will be updated to RED_WON or BLUE_WON.
		#    If not, then the game continues and update whose turn it is.
		# --------------------------------------------------------------------------------------------------------------

		# Make the indicated move

			# If there is an game piece in the toPosition, then remove it from the opponent's holding.
			# Put the Game Piece in the fromPosition in the toPosition.
			# Put None in the fromPosition

			# ----------------------------------------------------------------------------------------------------------
			# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
			# 7. Determining which player has won and also figuring out when to check that.
			#    Once it has been determined that the opponent has been checkmated,
			#    then the game has been won by the current player.
			#    The game status will be changed from UNFINISHED to RED_WON or BLUE_WON.
			# ----------------------------------------------------------------------------------------------------------

			# Check if the opponent has been checkmated by calling the is_checkmate method.
			# If so, then update the game state to either RED_WON or BLUE_WON
			# If not, then update whose turn it is by calling the switch_turn method.
		pass

	def print_board(self):
		"""Print the game board on the screen."""

		# Go through the dictionary (row, column)
			# Print empty space if there is no game piece at the position
			# Print the name of the game piece if the game piece exist
		# max_spaces = 8

		def cellForPrint(max_spaces, center, left_filler=' ', right_filler=' ', num_cell=1):
			"""Take the maxium number of spaces occupied, the string at the center,
			filler characters on the left and on the right, and the number of repeated cells as parameters.
			Returns the string that print a standardized cell for printing on the terminal."""
			left = (max_spaces - len(center)) // 2
			right = max_spaces - len(center) - left
			cell = left * left_filler + center + right * right_filler
			return cell * num_cell

		max_spaces = 13
		row_spaces = 5

		fortress_red = [(i, j) for i in range(0, 3) for j in range(3, 6)]
		fortress_blue = [(i, j) for i in range(7, 10) for j in range(3, 6)]
		fortress = fortress_red + fortress_blue

		row_spacer = cellForPrint(row_spaces, '')
		empty_space = {"other": cellForPrint(max_spaces, "[ ]", '-', '-'),
		               0: cellForPrint(max_spaces, "[ ]", ' ', '-'),
		               self._columns - 1: cellForPrint(max_spaces, "[ ]", '-', ' ')}

		empty_space_fortress = {3: cellForPrint(max_spaces, "[ ]", '-', '='),
		                        4: cellForPrint(max_spaces, "[ ]", '=', '='),
		                        5: cellForPrint(max_spaces, "[ ]", '=', '-')}

		empty_row = (row_spacer + cellForPrint(max_spaces, "|", num_cell=self._columns) + "\n") * 3
		empty_row_fortress = (row_spacer + cellForPrint(max_spaces, "|", num_cell=self._columns//2-1) + cellForPrint(max_spaces, "║", num_cell=self._columns//2-1) + cellForPrint(max_spaces, "|", num_cell=self._columns//2-1) + '\n') * 3

		print()
		print("ROW  " + cellForPrint(max_spaces, '', num_cell=4) + cellForPrint(max_spaces, "COLUMN", ' ', ' '))

		print(row_spacer, end="")
		for i in range(self._columns):
			print(cellForPrint(max_spaces, chr(i + 65), ' ', ' '), end="")
		print()


		for i in range(self._rows):
			print(cellForPrint(row_spaces, str(i + 1)), end="")

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
			print()
			if i == self._rows - 1:
				continue
			if i < 2 or i > 6:
				print(empty_row_fortress, end="")
			else:
				print(empty_row, end="")

class GamePiece:
	"""A class that represent individual game piece"""
	# Does not have set_player method as properties of the game piece cannot be changed.

	def __init__(self, player, identifier):
		"""Initiate the game piece."""
		# Player who own the piece, either RED or BLUE

		self._player = player
		self._identifier = identifier

	def get_player(self):
		"""Returns the player who own the piece."""
		return self._player

	def get_starting_position(self):
		"""Returns the starting position of the game piece based on what game piece it is, who owns the game piece, as well as the identifier of the game piece."""
		return self._starting_position[(self._player, self._name, self._identifier)]

	def get_name(self):
		"""Return the name of the game piece."""
		return self._name

	def print_name(self, max_space):
		"""Print the name of the game piece on screen with appropriate spacing."""

		if self._player == "RED":
			ANSI_code = 31
		elif self._player == "BLUE":
			ANSI_code = 34

		max_space -= 2
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
		self._starting_position = {("RED", "General", 0)    :   (1, 4),
		                           ("BLUE", "General", 0)   :   (8, 4)}

	def legal_moves(self, board, current_position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the General can play next."""
		pass

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
		pass

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
		Return all legal moves that the Guard can play next."""
		pass

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

	def legal_moves(self, board, position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Elephant can play next."""
		pass

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

	def legal_moves(self, board, position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Chariot can play next."""
		pass

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

	def legal_moves(self, board, position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Cannon can play next."""
		pass

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

	def legal_moves(self, board, position):
		"""Takes the board and the current position as parameters.
		Return all legal moves that the Soldier can play next."""
		pass

class InvalidPositionError(Exception):
	"""Raised when the input position of the board is invalid."""
	pass