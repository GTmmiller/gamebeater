from django.test import TestCase
from django.utils import timezone

from .models import Game, Console, Genre
from goals.models import Goal, GoalText

class GameMethodTests(TestCase):
	TEST_GAME_NAME = "Test Game"

	def test_get_goal_start_time_with_start_time_goal(self):
		"""
		get_goal_start_time should return the game's goal's start time with a game that has a goal with a valid start_time
		"""
		goal_start_time = timezone.now()
		test_game_with_start_time = Game(
			title=self.TEST_GAME_NAME,
			goal=Goal(start_time=goal_start_time)
		)
		self.assertEqual(test_game_with_start_time.get_goal_start_time(), goal_start_time)

	def test_get_goal_start_time_with_goal_none_start_time(self):
		"""
		get_goal_start_time should return None if the game's goal has a None start_time.
		"""
		test_game_with_goal = Game(
			title=self.TEST_GAME_NAME,
			goal=Goal()
		)
		self.assertEqual(test_game_with_goal.get_goal_start_time(), None)

	def test_get_goal_status_with_default_goal(self):
		"""
		get_goal_status should return the full default status when a game has a goal with the default status
		"""
		default_goal = Goal()
		test_game_with_goal = Game(
			title=self.TEST_GAME_NAME,
			goal=default_goal
		)
		self.assertEqual(test_game_with_goal.get_goal_status(), default_goal.get_status_display())

	def test_get_goal_status_with_specified_status(self):
		"""
		get_goal_status should return a full specified status when a game's goal is created with a specific status
		"""
		complete_goal = Goal(status=Goal.COMPLETE)
		test_game_with_status_goal = Game(
			title=self.TEST_GAME_NAME,
			goal=complete_goal
		)
		self.assertEqual(test_game_with_status_goal.get_goal_status(), complete_goal.get_status_display())

	def test_get_goal_complete_time_with_complete_time_goal(self):
		"""
		get_goal_complete_time should return the game's goal's complete time with a game that has a goal with a valid complete_time
		"""
		goal_complete_time = timezone.now()
		test_game_with_complete_time = Game(
			title=self.TEST_GAME_NAME,
			goal=Goal(complete_time=goal_complete_time)
		)
		self.assertEqual(test_game_with_complete_time.get_goal_complete_time(), goal_complete_time)

	def test_get_goal_complete_time_with_goal_none_complete_time(self):
		"""
		get_goal_complete_time should return None if the game's goal has a None complete_time.
		"""
		test_game_with_goal = Game(
			title=self.TEST_GAME_NAME,
			goal=Goal()
		)
		self.assertEqual(test_game_with_goal.get_goal_complete_time(), None)

	def test_get_goal_text_with_custom_text(self):
		"""
		get_goal_text should always return the goal text of a goal assigned to a game
		"""
		goal_text = "Custom goal"
		custom_goal_game = Game(
			title=self.TEST_GAME_NAME,
			goal=Goal(goal=GoalText(text=goal_text))
		)
		self.assertEqual(custom_goal_game.get_goal_text(), goal_text)
