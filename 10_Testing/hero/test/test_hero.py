from unittest import TestCase, main

from project.hero import Hero


class TestHero(TestCase):
    username = "Test Hero"
    level = 9
    health = 10.
    damage = 5.


    def setUp(self):
        self.hero = Hero(self.username,self.level , self.health, self.damage)

    def test_init(self):
        self.assertEqual(self.username, self.hero.username)
        self.assertEqual(self.health, self.hero.health)
        self.assertEqual(self.damage, self.hero.damage)
        self.assertEqual(self.level, self.hero.level)

    def test_attr_type(self):
        self.assertIsInstance(self.hero.username, str)
        self.assertIsInstance(self.hero.health, float)
        self.assertIsInstance(self.hero.damage, float)
        self.assertIsInstance(self.hero.level, int)

    def test_battle_enemy_same_name(self):
        enemy = Hero(self.username, self.level, self.health, self.damage)
        with self.assertRaises(Exception) as e:
            self.hero.battle(enemy)
        self.assertEqual("You cannot fight yourself", str(e.exception))

    def test_battle_hero_not_enough_health(self):
        self.hero.health = 0
        enemy = Hero("Enemy", self.level, 10, self.damage)
        with self.assertRaises(ValueError) as e:
            self.hero.battle(enemy)
        self.assertEqual("Your health is lower than or equal to 0. You need to rest", str(e.exception))

    def test_battle_hero_not_zerro_health(self):
        self.hero.health = -1 # <=
        enemy = Hero("Enemy", self.level, 10, self.damage)
        with self.assertRaises(ValueError) as e:
            self.hero.battle(enemy)
        self.assertEqual("Your health is lower than or equal to 0. You need to rest", str(e.exception))

    def test_draw(self):
        enemy = Hero("Enemy", self.level, self.health, self.damage)
        result = self.hero.battle(enemy)
        self.assertEqual("Draw", result)
        self.assertEqual(self.level, self.hero.level)
        self.assertEqual(-35, self.hero.health)
        self.assertEqual(self.damage, self.hero.damage)
        self.assertEqual("Draw", result)
        self.assertEqual(self.level, enemy.level)
        self.assertEqual(-35, enemy.health)
        self.assertEqual(self.damage, enemy.damage)

    def test_hero_win(self):
        enemy = Hero("Enemy", 1, 1, 1)
        result = self.hero.battle(enemy)
        self.assertEqual("You win", result)
        self.assertEqual(10, self.hero.level)
        self.assertEqual(14.0, self.hero.health)
        self.assertEqual(5.0, self.damage)

    def test_hero_lose(self):
        enemy = Hero("Enemy", 100, 100, 100)
        result = self.hero.battle(enemy)
        self.assertEqual("You lose", result)
        self.assertEqual(9, self.hero.level)
        self.assertEqual(-9990.0, self.hero.health)
        self.assertEqual(5.0, self.damage)

    def test_str(self):
        expected = f"Hero {self.username}: {self.level} lvl\n" \
               f"Health: {self.health}\n" \
               f"Damage: {self.damage}\n"
        self.assertEqual(expected, str(self.hero))




if __name__ == '__main__':
    main()