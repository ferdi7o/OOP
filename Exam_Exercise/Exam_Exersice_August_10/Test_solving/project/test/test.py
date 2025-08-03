from unittest import TestCase, main

from project.soccer_player import SoccerPlayer

class TestSoccerPlayer(TestCase):
    def setUp(self):
        self.player1 = SoccerPlayer("Player One", 34, 700, "PSG")
        self.player2 = SoccerPlayer("Player Two", 30, 750, "Juventus")

    def test_init(self):
        self.assertEqual("Player One", self.player1.name)
        self.assertEqual(34, self.player1.age)
        self.assertEqual(700, self.player1.goals)
        self.assertEqual("PSG", self.player1.team)
        self.assertEqual({}, self.player1.achievements)

    def test_name_validation(self):
        with self.assertRaises(ValueError) as e:
            self.player1.name = "One"
        self.assertEqual("Name should be more than 5 symbols!", str(e.exception))

    def test_age_validation(self):
        with self.assertRaises(ValueError) as e:
            self.player1.age = 12
        self.assertEqual("Players must be at least 16 years of age!", str(e.exception))

    def test_goals_validation(self):
        self.player1.goals = -1
        self.assertEqual(0, self.player1.goals)

    def test_team_validation(self):
        with self.assertRaises(ValueError) as e:
            self.player1.team = "BESIKTAS"
        self.assertEqual("Team must be one of the following: Barcelona, Real Madrid, Manchester United, Juventus, PSG!", str(e.exception))

    def test_change_to__valid_team(self):
        result = self.player1.change_team("Juventus")
        self.assertEqual("Juventus", self.player1.team)
        self.assertEqual("Team successfully changed!", result)

    def test_change_to__invalid_team(self):
        result = self.player1.change_team("BJK")
        self.assertEqual("PSG", self.player1.team)
        self.assertEqual("Invalid team name!", result)

    def test_add_new_achievement(self):
        result = self.player1.add_new_achievement("TOKYO")
        self.assertEqual("TOKYO has been successfully added to the achievements collection!", result)
        self.assertEqual(1, len(self.player1.achievements))
        self.assertEqual(1, self.player1.achievements["TOKYO"])

    def test_compare(self):
        self.assertEqual("Player Two is a top goal scorer! S/he scored more than Player One.",
                         self.player1 < self.player2)
        self.assertEqual("Player Two is a better goal scorer than Player One.",
                         self.player2 < self.player1)

if __name__ == '__main__':
    main()