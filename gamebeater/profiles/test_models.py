from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import GameOwnership, GamebeaterProfile, CompletionStatus, ObjectsByStatus, Goal
from games.models import Game, Genre, Platform
from .statuses import CompletionStatus, OwnershipStatus, ObjectsByStatus, get_all_objects_by_status


def create_game(game_title, genre_name="Test", platform_name="Testtendo 64"):
    """
	Creates a game with the passed in genre and platform. If the platform or genre doesn't exist create it too.
    """
    platform = Platform.objects.get_or_create(name=platform_name)[0]
    genre = Genre.objects.get_or_create(name=genre_name)[0]
    game = Game.objects.create(title=game_title)
    
    game.platforms.add(platform)
    game.genres.add(genre)

    return game


def create_test_profile():
    """
    Create a gamebeater profile with a pre-determined test user
    """
    user = get_user_model().objects.create(
        username="TestUser",
        email="test@user.org",
        password="testpassword"
    )
    user.set_password(user.password)
    user.save()
    return GamebeaterProfile.objects.create(user=user)


def create_ownership(profile, game, ownership_status=OwnershipStatus.WANTS, completion_status=CompletionStatus.ON_HOLD):
    """
    Create a GameOwnership object between the passed in profile and game. An ownership status and completion status can also be passed in though they have default values.
    """
    return GameOwnership.objects.create(
        owner=profile,
        game=game,
        platform=game.platforms.first(),
        ownership_status=ownership_status,
        completion_status=completion_status
    )


class GamebeaterProfileMethodTests(TestCase):

    def test_get_gameownerships_by_completion_with_no_games(self):
        """
        get_gameownerships_by_completion should return an empty list if there are no games with with the inputted completion status.
        """
        profile = create_test_profile()

        self.assertEqual(
            [],
            list(profile.get_gameownerships_by_completion(CompletionStatus.IN_PROGRESS))
        )

    def test_get_gameownerships_by_completion_with_wrong_status(self):
        """
        get_gameownerships_by_completion should return an empty list if the completion status inputted is not valid.
        """
        profile = create_test_profile()
        game = create_game(game_title="TestGame")
        ownership = create_ownership(
            profile=profile,
            game=game
        )
        
        self.assertEqual(
            [],
            list(profile.get_gameownerships_by_completion('Z'))
        )
    
    def test_get_gameownerships_by_completion_with_games(self):
        """
        get_gameownerships_by_completion should return all games with the inputted completion status.
        """
        profile = create_test_profile()
        game_one = create_game(game_title="TestGame")
        game_two = create_game(game_title="TestGame 2: Revenge")
        game_three = create_game(game_title="TestGame 3: Final Mix")

        ownership_one = create_ownership(profile=profile, game=game_one)
        ownership_two = create_ownership(profile=profile, game=game_two)
        ownership_three = create_ownership(
            profile=profile,
            game=game_three,
            completion_status=CompletionStatus.COMPLETE
        )

        query_set = profile.get_gameownerships_by_completion(CompletionStatus.ON_HOLD)

        self.assertIn(ownership_one, query_set)
        self.assertIn(ownership_two, query_set)
        self.assertNotIn(ownership_three, query_set)

    def test_get_unaffiliated_games_with_no_games(self):
        """
        get_unaffiliated_games should return a blank query set with no games
        """
        profile = create_test_profile()
        self.assertFalse(profile.get_unaffiliated_games())

    def test_get_unaffiliated_games_with_no_owned_games(self):
        """
        get_unaffiliated_games should return all games when no games are owned
        """
        profile = create_test_profile()

        create_game(game_title="TestGame")
        create_game(game_title="TestGame 2: Revenge")
        create_game(game_title="TestGame 3: Final Mix")

        self.assertEqual(
            list(Game.objects.all()),
            list(profile.get_unaffiliated_games())
        )

    def test_get_unaffiliated_games_with_unowned_games(self):
        """
        get_unaffiliated_games should return a query with games not owned when the user already
        owns some games
        """
        profile = create_test_profile()

        game_one = create_game(game_title="TestGame")
        game_two = create_game(game_title="TestGame 2: Revenge")
        game_three = create_game(game_title="TestGame 3: Final Mix")

        create_ownership(profile=profile, game=game_one)

        query_set = profile.get_unaffiliated_games()

        self.assertNotIn(game_one, query_set)
        self.assertIn(game_two, query_set)
        self.assertIn(game_three, query_set)

    def test_get_unaffiliated_games_with_all_games_owned(self):
        """
        get_unaffiliated_games should return a blank query set when all games are owned
        """
        profile = create_test_profile()

        game_one = create_game(game_title="TestGame")
        game_two = create_game(game_title="TestGame 2: Revenge")
        game_three = create_game(game_title="TestGame 3: Final Mix")

        create_ownership(profile=profile, game=game_one)
        create_ownership(profile=profile, game=game_two)
        create_ownership(profile=profile, game=game_three)

        self.assertEqual([], list(profile.get_unaffiliated_games()))

class GameOwnershipMethodsTests(TestCase):

    def setUp(self):
        self.test_ownership = create_ownership(
            profile=create_test_profile(),
            game=create_game(game_title="Test_Game")
        )

    def test_get_goals_by_completion_with_no_goals(self):
        """
        get_goals_by_completion should return an empty list if there are no goals with the inputted completion status.
        """
        self.assertEqual(
            [],
            list(self.test_ownership.get_goals_by_completion(CompletionStatus.IN_PROGRESS))
        )

    def test_get_goals_by_completion_with_wrong_status(self):
        """
        get_goals_by_completion should return an empty list if the completion status inputted is not valid.
        """
        Goal.objects.create(
            ownership=self.test_ownership,
            text="Test Goal",
            status=CompletionStatus.IN_PROGRESS
        )

        self.assertEqual(
            [],
            list(self.test_ownership.get_goals_by_completion('Z'))
        )

    def test_get_goals_by_completion_with_goals(self):
        """
        get_goals_by_completion should return all goals with the inputted completion status.
        """
        goal_in_progress = Goal.objects.create(
            ownership=self.test_ownership,
            text="Test_Goal",
            status=CompletionStatus.IN_PROGRESS
        )
        goal_complete = Goal.objects.create(
            ownership=self.test_ownership,
            text="Test_Goal_2",
            status=CompletionStatus.COMPLETE
        )

        query_set = self.test_ownership.get_goals_by_completion(CompletionStatus.IN_PROGRESS)

        self.assertIn(goal_in_progress, query_set)
        self.assertNotIn(goal_complete, query_set)
        self.assertEqual(1, query_set.count())

class ObjectsByStatusMethodTests(TestCase):
    
    def setUp(self):
        self.test_user = create_test_profile()
        create_ownership(profile=self.test_user, game=create_game(game_title="TestGame"))
        create_ownership(profile=self.test_user, game=create_game(game_title="TestGame 2"))
        create_ownership(
            profile=self.test_user, 
            game=create_game(game_title="TestGame 3"),
            completion_status=CompletionStatus.COMPLETE
        )
    
    def test___init___with_zero_gametotal(self):
        """
        ObjectsByStatus should have a status_percentage of 0 if
        zero is passed as the object_total
        """
        ownerships_by_completion_status = ObjectsByStatus(
            status=CompletionStatus.NOT_STARTED, 
            object_list=self.test_user.gameownership_set.all(),
            object_total=0
        )
        self.assertEqual(0, ownerships_by_completion_status.status_percentage)

    def test___init___with_positive_gametotal(self):
        """
        ObjectsByStatus should have a correct status_percentage if a
        positive object_total is passed
        """
        ownerships_by_completion_status = ObjectsByStatus(
            status=CompletionStatus.COMPLETE,
            object_list=self.test_user.gameownership_set.filter(completion_status=CompletionStatus.COMPLETE),
            object_total=GameOwnership.objects.count() 
        )
        self.assertEqual(33, ownerships_by_completion_status.status_percentage)

class GetAllObjectsByStatusTests(TestCase):
    def setUp(self):
        self.test_profile = create_test_profile()

    def test_get_all_objects_by_status_with_gameownerships_and_completion_status_with_no_ownerships(self):
        all_gameownerships_by_completion = get_all_objects_by_status(
            objects = self.test_profile.games,
            status_class = CompletionStatus,
            object_by_status_method = self.test_profile.get_gameownerships_by_completion
        )
        self.assertEqual(len(OwnershipStatus.CHOICES), len(all_gameownerships_by_completion))
        for index, choice in enumerate(CompletionStatus.CHOICES):
            self.assertEqual(choice[1], all_gameownerships_by_completion[index].status)
            self.assertEqual(
                list(self.test_profile.gameownership_set.filter(completion_status=choice[0])), 
                list(all_gameownerships_by_completion[index].object_list)
            )

    def test_get_all_objects_by_status_with_gameownerships_and_completion_status_with_ownerships(self):
        game_one = create_game(game_title="TestGame")
        game_two = create_game(game_title="TestGame 2: Revenge")
        game_three = create_game(game_title="TestGame 3: Final Mix")
        game_four = create_game(game_title="TestGame 4: Final Final Mix")
        game_five = create_game(game_title="TestGame 5: The Return")
        game_six = create_game(game_title="TestGame 6: The Remix")

        create_ownership(profile=self.test_profile, game=game_one, completion_status=CompletionStatus.NOT_STARTED)
        create_ownership(profile=self.test_profile, game=game_two, completion_status=CompletionStatus.NOT_STARTED)
        create_ownership(profile=self.test_profile, game=game_three, completion_status=CompletionStatus.IN_PROGRESS)
        create_ownership(profile=self.test_profile, game=game_four, completion_status=CompletionStatus.ON_HOLD)
        create_ownership(profile=self.test_profile, game=game_five, completion_status=CompletionStatus.COMPLETE)
        create_ownership(profile=self.test_profile, game=game_six, completion_status=CompletionStatus.COMPLETE)

        completion_choices_text = [choice[1] for choice in CompletionStatus.CHOICES]
        all_gameownerships_by_completion = get_all_objects_by_status(
            objects = self.test_profile.games,
            status_class = CompletionStatus,
            object_by_status_method = self.test_profile.get_gameownerships_by_completion
        )

        self.assertEqual(len(OwnershipStatus.CHOICES), len(all_gameownerships_by_completion))
        for index, choice in enumerate(CompletionStatus.CHOICES):
            self.assertEqual(choice[1], all_gameownerships_by_completion[index].status)
            self.assertEqual(
                list(self.test_profile.gameownership_set.filter(completion_status=choice[0])), 
                list(all_gameownerships_by_completion[index].object_list)
            )