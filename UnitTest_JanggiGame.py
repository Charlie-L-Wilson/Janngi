import unittest
from JanggiGame import JanggiGame, GamePiece, General, Guard, Horse, Elephant, Chariot, Cannon, Soldier, InvalidPositionError

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

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_red_player_0.get_player(), "RED")
		self.assertEqual(test_blue_player_0.get_player(), "BLUE")

	def test_get_identifier(self):
		"""Testing the get_identifier method for the General"""
		test_blue_player_0 = General("BLUE", 0)
		self.assertEqual(test_blue_player_0.get_identifier(), 0)

	def test_get_name(self):
		"""Testing the get_name method for the General"""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_red_player_0.get_name(), "General")
		self.assertEqual(test_blue_player_0.get_name(), "General")

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the General"""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_blue_player_0.get_starting_position(), (8, 4))
		self.assertEqual(test_red_player_0.get_starting_position(), (1, 4))

	def test_get_fortress(self):
		"""Testing the get_fortress method."""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		red_fortress = {(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)}
		blue_fortress = {(7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5), (9, 3), (9, 4), (9, 5)}
		test_red_fortress = test_red_player_0.get_fortress()
		test_blue_fortress = test_blue_player_0.get_fortress()

		self.assertEqual(test_red_fortress, red_fortress)
		self.assertEqual(test_blue_fortress, blue_fortress)

	def test_get_diagonalMoves(self):
		"""Testing the get_diagonalMoves method."""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_red_player_0.get_diagonalMoves((1, 4)), {(0, 3), (0, 5), (2, 3), (2, 5)})
		self.assertEqual(test_blue_player_0.get_diagonalMoves((7, 5)), {(8, 4)})

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

class TestGuard(unittest.TestCase):
	"""Testing the Guard class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Guards."""

		test_red_guard_0 = Guard("RED", 0)
		test_red_guard_1 = Guard("RED", 1)
		test_blue_guard_0 = Guard("BLUE", 0)
		test_blue_guard_1 = Guard("BLUE", 1)

		self.assertEqual(test_red_guard_0.get_starting_position(), (0, 3))
		self.assertEqual(test_red_guard_1.get_starting_position(), (0, 5))
		self.assertEqual(test_blue_guard_0.get_starting_position(), (9, 3))
		self.assertEqual(test_blue_guard_1.get_starting_position(), (9, 5))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Guards."""

		game = JanggiGame()
		test_red_guard_0 = game.get_players()["RED"][1]
		test_red_guard_1 = game.get_players()["RED"][2]
		test_blue_guard_0 = game.get_players()["BLUE"][1]
		test_blue_guard_1 = game.get_players()["BLUE"][2]

		self.assertEqual(test_red_guard_0.legal_moves(game.get_board(), game.get_position(test_red_guard_0)), {(0, 4), (1, 3)})
		self.assertEqual(test_red_guard_1.legal_moves(game.get_board(), game.get_position(test_red_guard_1)), {(0, 4), (1, 5)})
		self.assertEqual(test_blue_guard_0.legal_moves(game.get_board(), game.get_position(test_blue_guard_0)), {(8, 3), (9, 4)})
		self.assertEqual(test_blue_guard_1.legal_moves(game.get_board(), game.get_position(test_blue_guard_1)), {(8, 5), (9, 4)})

		# Moving the Red General to (2, 4)
		game._board[(2, 4)] = game._board[(1, 4)]
		game._board[(1, 4)] = None
		self.assertEqual(test_red_guard_0.legal_moves(game.get_board(), game.get_position(test_red_guard_0)), {(0, 4), (1, 3), (1, 4)})

		# Moving the Guard 0 to (1, 4). Red General is still at (2, 4)
		game._board[(1, 4)] = game._board[(0, 3)]
		game._board[(0, 3)] = None
		self.assertEqual(test_red_guard_0.legal_moves(game.get_board(), game.get_position(test_red_guard_0)), {(0, 3), (0, 4), (1, 3), (1, 5), (2, 3), (2, 5)})

class TestHorse(unittest.TestCase):
	"""Testing the Horse class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Horse."""

		test_red_horse_0 = Horse("RED", 0)
		test_red_horse_1 = Horse("RED", 1)
		test_blue_horse_0 = Horse("BLUE", 0)
		test_blue_horse_1 = Horse("BLUE", 1)

		self.assertEqual(test_red_horse_0.get_starting_position(), (0, 2))
		self.assertEqual(test_red_horse_1.get_starting_position(), (0, 7))
		self.assertEqual(test_blue_horse_0.get_starting_position(), (9, 2))
		self.assertEqual(test_blue_horse_1.get_starting_position(), (9, 7))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Horses."""

		game = JanggiGame()
		test_red_horse_0 = game.get_players()["RED"][3]
		test_red_horse_1 = game.get_players()["RED"][4]
		test_blue_horse_0 = game.get_players()["BLUE"][3]
		test_blue_horse_1 = game.get_players()["BLUE"][4]

		self.assertEqual(test_red_horse_0.legal_moves(game.get_board(), game.get_position(test_red_horse_0)), {(2, 3)})
		self.assertEqual(test_red_horse_1.legal_moves(game.get_board(), game.get_position(test_red_horse_1)), {(2, 6), (2, 8)})
		self.assertEqual(test_blue_horse_0.legal_moves(game.get_board(), game.get_position(test_blue_horse_0)), {(7, 3)})
		self.assertEqual(test_blue_horse_1.legal_moves(game.get_board(), game.get_position(test_blue_horse_1)), {(7, 6), (7, 8)})

		# Moving Red Horse 1 to (2, 3)
		game._board[(2, 3)] = game._board[(0, 2)]
		game._board[(0, 2)] = None
		self.assertEqual(test_red_horse_0.legal_moves(game.get_board(), game.get_position(test_red_horse_0)), {(0, 2), (1, 1), (3, 1), (4, 2), (4, 4), (3, 5), (1, 5), (0, 4)})

		# Moving Blue Horse 1 to (3, 3) and Blue Horse 2 to (3, 1)
		game._board[(3, 3)] = game._board[(9, 2)]
		game._board[(9, 2)] = None
		game._board[(3, 1)] = game._board[(9, 7)]
		game._board[(9, 7)] = None
		self.assertEqual(test_red_horse_0.legal_moves(game.get_board(), game.get_position(test_red_horse_0)), {(0, 2), (1, 1), (3, 1), (3, 5), (1, 5), (0, 4)})

class TestElephant(unittest.TestCase):
	"""Testing the Elephant class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Elephant."""

		test_red_Elephant_0 = Elephant("RED", 0)
		test_red_Elephant_1 = Elephant("RED", 1)
		test_blue_Elephant_0 = Elephant("BLUE", 0)
		test_blue_Elephant_1 = Elephant("BLUE", 1)

		self.assertEqual(test_red_Elephant_0.get_starting_position(), (0, 1))
		self.assertEqual(test_red_Elephant_1.get_starting_position(), (0, 6))
		self.assertEqual(test_blue_Elephant_0.get_starting_position(), (9, 1))
		self.assertEqual(test_blue_Elephant_1.get_starting_position(), (9, 6))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Elephant."""

		game = JanggiGame()
		test_red_Elephant_0 = game.get_players()["RED"][5]
		test_red_Elephant_1 = game.get_players()["RED"][6]
		test_blue_Elephant_0 = game.get_players()["BLUE"][5]
		test_blue_Elephant_1 = game.get_players()["BLUE"][6]

		self.assertEqual(test_red_Elephant_0.legal_moves(game.get_board(), game.get_position(test_red_Elephant_0)),
		                 {(3, 3)})
		self.assertEqual(test_red_Elephant_1.legal_moves(game.get_board(), game.get_position(test_red_Elephant_1)),
		                 set())
		self.assertEqual(test_blue_Elephant_0.legal_moves(game.get_board(), game.get_position(test_blue_Elephant_0)),
		                 {(6, 3)})
		self.assertEqual(test_blue_Elephant_1.legal_moves(game.get_board(), game.get_position(test_blue_Elephant_1)),
		                 set())

		# Moving the Red Elephant 1 to (3, 3)
		game._board[(3, 3)] = game._board[(0, 1)]
		game._board[(0, 1)] = None
		self.assertEqual(test_red_Elephant_0.legal_moves(game.get_board(), game.get_position(test_red_Elephant_0)),
		                 {(0, 1), (6, 1), (6, 5)})

		# Red Element Remain at (3, 3)
		# Moving Blue Elephant 2 to (6, 5) - illegal move but just for testing
		game._board[(6, 5)] = game._board[(9, 6)]
		game._board[(9, 6)] = None

		self.assertEqual(test_red_Elephant_0.legal_moves(game.get_board(), game.get_position(test_red_Elephant_0)), {(0, 1), (6, 1), (6, 5)})
		self.assertEqual(test_blue_Elephant_1.legal_moves(game.get_board(), game.get_position(test_blue_Elephant_1)), {(3, 3), (3, 7)})

class TestChariot(unittest.TestCase):
	"""Testing the Chariot class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Chariot."""

		test_red_Chariot_0 = Chariot("RED", 0)
		test_red_Chariot_1 = Chariot("RED", 1)
		test_blue_Chariot_0 = Chariot("BLUE", 0)
		test_blue_Chariot_1 = Chariot("BLUE", 1)

		self.assertEqual(test_red_Chariot_0.get_starting_position(), (0, 0))
		self.assertEqual(test_red_Chariot_1.get_starting_position(), (0, 8))
		self.assertEqual(test_blue_Chariot_0.get_starting_position(), (9, 0))
		self.assertEqual(test_blue_Chariot_1.get_starting_position(), (9, 8))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Chariot."""

		game = JanggiGame()
		test_red_Chariot_0 = game.get_players()["RED"][7]
		test_red_Chariot_1 = game.get_players()["RED"][8]
		test_blue_Chariot_0 = game.get_players()["BLUE"][7]
		test_blue_Chariot_1 = game.get_players()["BLUE"][8]

		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)), {(1, 0), (2, 0)})
		self.assertEqual(test_red_Chariot_1.legal_moves(game.get_board(), game.get_position(test_red_Chariot_1)), {(1, 8), (2, 8)})
		self.assertEqual(test_blue_Chariot_0.legal_moves(game.get_board(), game.get_position(test_blue_Chariot_0)), {(7, 0), (8, 0)})
		self.assertEqual(test_blue_Chariot_1.legal_moves(game.get_board(), game.get_position(test_blue_Chariot_1)), {(7, 8), (8, 8)})

		# Move Red Chariot 1 to (7, 3) and Blue General to (9, 4)
		game._board[(7, 3)] = game._board[(0, 0)]
		game._board[(0, 0)] = None
		game._board[(9, 4)] = game._board[(8, 4)]
		game._board[(8, 4)] = None

		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)), {(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (8, 3), (9, 3), (7, 2), (7, 1), (7, 4), (7, 5), (7, 6), (7, 7), (8, 4), (9, 5)})

		# Moving Red Chariot 2 to (9, 5)
		game._board[(9, 5)] = game._board[(0, 8)]
		game._board[(0, 8)] = None

		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)), {(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (8, 3), (9, 3), (7, 2), (7, 1), (7, 4),
		                                                                                                           (7, 5), (7, 6), (7, 7), (8, 4)})

		# Move Red Chariot 1 to (8, 4)
		game._board[(8, 4)] = game._board[(7, 3)]
		game._board[(7, 3)] = None
		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)), {(8, 0), (8, 1), (8, 2), (8, 3), (8, 5), (8, 6), (8, 7), (8, 8), (7, 4), (6, 4), (7, 3), (7, 5), (9, 3), (9, 4)})

class TestCannon(unittest.TestCase):
	"""Testing the Cannon class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Cannon."""

		test_red_cannon_0 = Cannon("RED", 0)
		test_red_cannon_1 = Cannon("RED", 1)
		test_blue_cannon_0 = Cannon("BLUE", 0)
		test_blue_cannon_1 = Cannon("BLUE", 1)

		self.assertEqual(test_red_cannon_0.get_starting_position(), (2, 1))
		self.assertEqual(test_red_cannon_1.get_starting_position(), (2, 7))
		self.assertEqual(test_blue_cannon_0.get_starting_position(), (7, 1))
		self.assertEqual(test_blue_cannon_1.get_starting_position(), (7, 7))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Cannons."""

		game = JanggiGame()
		test_red_cannon_0 = game.get_players()["RED"][9]
		test_red_cannon_1 = game.get_players()["RED"][10]
		test_blue_cannon_0 = game.get_players()["BLUE"][9]
		test_blue_cannon_1 = game.get_players()["BLUE"][10]

		self.assertEqual(test_red_cannon_0.legal_moves(game.get_board(), game.get_position(test_red_cannon_0)), set())
		self.assertEqual(test_red_cannon_1.legal_moves(game.get_board(), game.get_position(test_red_cannon_1)), set())
		self.assertEqual(test_blue_cannon_0.legal_moves(game.get_board(), game.get_position(test_blue_cannon_0)), set())
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)), set())

		# Moving Red Cannon 1 to (2, 4)
		game._board[(2, 4)] = game._board[(2, 1)]
		game._board[(2, 1)] = None
		self.assertEqual(test_red_cannon_0.legal_moves(game.get_board(), game.get_position(test_red_cannon_0)), {(0, 4), (4, 4), (5, 4), (6, 4)})

		# Moving Red Cannon 2 to (3, 7)
		game._board[(3, 7)] = game._board[(2, 7)]
		game._board[(2, 7)] = None
		self.assertEqual(test_red_cannon_1.legal_moves(game.get_board(), game.get_position(test_red_cannon_1)), {(3, 5)})

		# Moving Blue Cannon 2 to (7, 5)
		game._board[(7, 5)] = game._board[(7, 7)]
		game._board[(7, 7)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)), set())

		# Moving Blue Guard 1 to (9, 4)
		game._board[(9, 4)] = game._board[(9, 3)]
		game._board[(9, 3)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)), {(9, 3)})

		# Moving Blue General to (8, 5)
		game._board[(8, 5)] = game._board[(8, 4)]
		game._board[(8, 4)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)), set())

		# Moving Red Cannon 1 to (8, 4)
		game._board[(8, 4)] = game._board[(2, 4)]
		game._board[(2, 4)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)), set())

		# Moving Red Cannon 2 to (3, 5)
		game._board[(3, 5)] = game._board[(3, 7)]
		game._board[(3, 7)] = None
		self.assertEqual(test_red_cannon_1.legal_moves(game.get_board(), game.get_position(test_red_cannon_1)), {(3, 3), (3, 7)})
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)), set())

		# Moving Blue Guard 1 to (8, 4)
		game._board[(8, 4)] = game._board[(9, 4)]
		game._board[(9, 4)] = None
		# Moving Red Cannon 2 to (9, 3)
		game._board[(9, 3)] = game._board[(3, 5)]
		game._board[(3, 5)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)), set())



if __name__ == "__main__":
	unittest.main()