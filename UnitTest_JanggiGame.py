import unittest
from JanggiGame import JanggiGame, GamePiece, General, Guard, Horse, Chariot, Cannon, Soldier, InvalidPositionError

class TestJanggiGame(unittest.TestCase):
	"""Testing the JanggiGame class"""

	def test_init(self):
		"""Testing the instantiation of the board."""

		game = JanggiGame()

		self.assertEqual(game._rows, 10)
		self.assertEqual(game._columns, 9)

		self.assertEqual(game._turn, "BLUE")
		self.assertEqual(game._status, "UNFINISHED")

		test_positions = [[None for j in range(game._columns)] for i in range(game._rows)]

		for i in range(game._rows):
			for j in range(game._columns):
				if game._board[(i, j)]:
					test_positions[i][j] = game._board[(i, j)].get_name()

					if i < 4:
						self.assertEqual(game._board[(i, j)].get_player(), "RED")
					elif i > 5:
						self.assertEqual(game._board[(i, j)].get_player(), "BLUE")

		correct_positions = [["Chariot", "Elephant", "Horse", "Guard", None, "Guard", "Elephant", "Horse", "Chariot"],
							 [None, None, None, None, "General", None, None, None, None],
							 [None, "Cannon", None, None, None, None, None, "Cannon", None],
							 ["Soldier", None, "Soldier", None, "Soldier", None, "Soldier", None, "Soldier"],
							 [None, None, None, None, None, None, None, None, None],
							 [None, None, None, None, None, None, None, None, None],
							 ["Soldier", None, "Soldier", None, "Soldier", None, "Soldier", None, "Soldier"],
							 [None, "Cannon", None, None, None, None, None, "Cannon", None],
							 [None, None, None, None, "General", None, None, None, None],
							 ["Chariot", "Elephant", "Horse", "Guard", None, "Guard", "Elephant", "Horse", "Chariot"]]

		self.assertEqual(test_positions, correct_positions)

		self.assertIn("BLUE", game._players)
		self.assertIn("RED", game._players)

		test_blue_player = [game_piece.get_name() for game_piece in game._players["BLUE"]]
		test_red_player = [game_piece.get_name() for game_piece in game._players["RED"]]

		correct_player = ["General"] + ["Guard"] * 2 + ["Horse"] * 2 + ["Elephant"] * 2 + \
		                 ["Chariot"] * 2 + ["Cannon"] * 2 + ["Soldier"] * 5

		self.assertEqual(test_blue_player, correct_player)
		self.assertEqual(test_red_player, correct_player)

	def test_get_rows(self):
		"""Testing the get_rows method"""

		game = JanggiGame()
		self.assertEqual(game.get_rows(), 10)

	def test_get_columns(self):
		"""Testing the get_rows method"""

		game = JanggiGame()
		self.assertEqual(game.get_columns(), 9)

	def test_get_board(self):
		"""Testing the get_board method"""

		game = JanggiGame()
		self.assertEqual(game.get_board(), game._board)
		self.assertEqual(len(game.get_board()), 90)

	def test_players(self):
		"""Testing the get_players"""

		game = JanggiGame()
		self.assertEqual(game.get_players(), game._players)
		self.assertEqual(len(game.get_players()), 2)
		self.assertIn("BLUE", game.get_players())
		self.assertIn("RED", game.get_players())
		self.assertEqual(len(game.get_players()["BLUE"]), 16)
		self.assertEqual(len(game.get_players()["RED"]), 16)

	def test_get_game_state(self):

		game = JanggiGame()
		self.assertEqual(game.get_game_state(), "UNFINISHED")

		game._status = "RED_WON"
		self.assertEqual(game.get_game_state(), "RED_WON")

		game._status = "BLUE_WON"
		self.assertEqual(game.get_game_state(), "BLUE_WON")

	def test_get_position(self):
		"""Testing the get_position method"""

		game = JanggiGame()
		for player in game.get_players():
			for gamePiece in game.get_players()[player]:
				position = game.get_position(gamePiece)
				self.assertIs(game.get_board()[position], gamePiece)

	def test_convert_position(self):
		"""Testing the convert_position_to_tuple and convert_position_to_string method"""

		game = JanggiGame()

		with self.assertRaises(InvalidPositionError):
			game.convert_position_to_tuple("A11")

		with self.assertRaises(InvalidPositionError):
			game.convert_position_to_tuple("A")

		with self.assertRaises(InvalidPositionError):
			game.convert_position_to_tuple("Z1")

		with self.assertRaises(InvalidPositionError):
			game.convert_position_to_tuple("AA")

		with self.assertRaises(InvalidPositionError):
			game.convert_position_to_tuple("11")

		with self.assertRaises(InvalidPositionError):
			game.convert_position_to_tuple("A11")

		self.assertEqual(game.convert_position_to_tuple("A1"), (0, 0))
		self.assertEqual(game.convert_position_to_tuple("E5"), (4, 4))
		self.assertEqual(game.convert_position_to_tuple("e6"), (5, 4))
		self.assertEqual(game.convert_position_to_tuple("I10"), (9, 8))

		self.assertEqual(game.convert_position_to_string((0, 0)), "A1")
		self.assertEqual(game.convert_position_to_string((4, 4)), "E5")
		self.assertEqual(game.convert_position_to_string((5, 4)), "E6")
		self.assertEqual(game.convert_position_to_string((9, 8)), "I10")

	def test_switch_turn(self):
		"""Testing the switch_turn method."""

		game = JanggiGame()
		self.assertEqual(game.switch_turn("BLUE"), "RED")
		self.assertEqual(game.switch_turn("RED"), "BLUE")

	def test_print_board(self):
		"""Testing the print_board method."""

		game = JanggiGame()
		# game.print_board()



class TestGeneral(unittest.TestCase):
	"""Testing the General class."""

	def test_get_player(self):
		"""Testing the get_player method for the General"""

		test_blue_player_0 = General("BLUE", 0)
		test_red_player_0 = General("RED", 0)

		self.assertEqual(test_blue_player_0.get_player(), "BLUE")
		self.assertEqual(test_red_player_0.get_player(), "RED")

	def test_get_name(self):
		"""Testing the get_name method for the General"""

		test_blue_player_0 = General("BLUE", 0)
		test_red_player_0 = General("RED", 0)

		self.assertEqual(test_blue_player_0.get_name(), "General")
		self.assertEqual(test_red_player_0.get_name(), "General")

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the General"""

		test_blue_player_0 = General("BLUE", 0)
		test_red_player_0 = General("RED", 0)

		self.assertEqual(test_blue_player_0.get_starting_position(), (8, 4))
		self.assertEqual(test_red_player_0.get_starting_position(), (1, 4))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the General"""

		game = JanggiGame()
		red_general = game.get_players()["RED"][0]
		blue_general = game.get_players()["BLUE"][0]

		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		test_blue_general_moves = blue_general.legal_moves(game.get_board(), game.get_position(blue_general))
		self.assertEqual(test_red_general_moves, {(0, 4), (1, 3), (1, 5), (2, 3), (2, 4), (2, 5)})
		self.assertEqual(test_blue_general_moves, {(9, 4), (8, 3), (8, 5), (7, 3), (7, 4), (7, 5)})

		# Move Red General to (2, 5)
		game._board[(2, 5)] = game._board[(1, 4)]
		game._board[(1, 4)] = None
		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		self.assertEqual(test_red_general_moves, {(1, 4), (1, 5), (2, 4)})

		# Move Blue General to (9, 4)
		game._board[(9, 4)] = game._board[(8, 4)]
		game._board[(8, 4)] = None
		test_blue_general_moves = blue_general.legal_moves(game.get_board(), game.get_position(blue_general))
		self.assertEqual(test_blue_general_moves, {(8, 4)})

		# Move Blue Soldier to (1, 4), Red General is still in (2, 5)
		game._board[(1, 4)] = game._board[(6, 4)]
		game._board[(6, 4)] = None
		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		self.assertEqual(test_red_general_moves, {(1, 4), (1, 5), (2, 4)})

		# Move Red General to (1, 5), Blue Soldier is still at (1, 4)
		game._board[(1, 5)] = game._board[(2, 5)]
		game._board[(2, 5)] = None
		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		self.assertEqual(test_red_general_moves, {(1, 4), (2, 5)})





if __name__ == "__main__":
	unittest.main()