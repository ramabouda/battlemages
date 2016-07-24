from django.test import TestCase
from battlemages.core.mages.models import Mage
from battlemages.core.players.models import Player
from battlemages.core.spells.models import Deck
from .models import Game, MageInGame, Card
from .exceptions import HasMoved, OutOfRange, OutOfBoundaries, LocationNotAvailable

class InitGameTestCase(TestCase):
    "tests about setting up and destroying the game"
    fixtures = ['test_fixtures.yaml']

    def setUp(self):
        self.m_termi = Mage.objects.get(name="Termifire")
        self.m_omega = Mage.objects.get(name="OmegaMax")
        self.p_toto = Player.objects.get(username="toto")
        self.p_titi = Player.objects.get(username="titi")

    def testCreateDestroyGame(self):
        ms_termi = MageInGame.from_mage(self.m_termi)
        ms_omega = MageInGame.from_mage(self.m_omega)

        self.assertFalse(Card.objects.exists())
        ms_termi.use_deck(Deck.objects.get(name="deck de feu"))
        ms_omega.use_deck(Deck.objects.get(name="deck mouillé"))
        self.assertTrue(Card.objects.exists())

        self.assertIsNone(ms_termi.location_x)
        self.assertIsNone(ms_termi.game)
        self.assertIsNone(ms_termi.team)
        game = Game.new_game(
            player_1=self.p_toto,
            player_2=self.p_titi,
            mages_p1=[ms_termi,],
            mages_p2=[ms_omega,]
        )
        self.assertIsNotNone(ms_termi.location_x)
        self.assertEqual(ms_termi.game, game)
        self.assertNotEqual(ms_termi.team, ms_omega.team)
        self.assertEqual(ms_termi.team + ms_omega.team, 3)

        # cascading delete
        game.delete()
        self.assertFalse(Card.objects.exists())
        self.assertFalse(MageInGame.objects.exists())


class MovementTestCase(TestCase):
    fixtures = ['test_fixtures.yaml']

    def setUp(self):
        m_termi = Mage.objects.get(name="Termifire")
        m_omega = Mage.objects.get(name="OmegaMax")
        p_toto = Player.objects.get(username="toto")
        p_titi = Player.objects.get(username="titi")
        self.ms_termi = MageInGame.from_mage(m_termi)
        self.ms_omega = MageInGame.from_mage(m_omega)

        self.ms_termi.use_deck(Deck.objects.get(name="deck de feu"))
        self.ms_omega.use_deck(Deck.objects.get(name="deck mouillé"))
        self.game = Game.new_game(
            player_1=p_toto,
            player_2=p_titi,
            mages_p1=[self.ms_termi,],
            mages_p2=[self.ms_omega,]
        )
        self.ms_termi.location = (4, 5)
        self.ms_termi.save()

    def testSimpleMove(self):
        self.game.move(self.ms_termi, (4, 6))
        self.assertEqual(self.ms_termi.location_x, 4)
        self.assertEqual(self.ms_termi.location_y, 6)

    def testDistance(self):
        self.assertEqual(self.game.get_distance(self.ms_termi, self.ms_omega), 1)
        self.ms_termi.location = (2, 1)
        self.assertEqual(self.game.get_distance(self.ms_termi, self.ms_omega), 4)
        self.ms_termi.location = (7, 2)
        self.assertEqual(self.game.get_distance(self.ms_termi, self.ms_omega), 3)


    def testMoveOutOfRange(self):
        with self.assertRaises(OutOfRange):
            self.game.move(self.ms_termi, (2, 1))

    def testMoveOutOfBoundaries(self):
        self.ms_termi.location = (0, 6)
        with self.assertRaises(OutOfBoundaries):
            self.game.move(self.ms_termi, (-1, 6))

    def testMoveOnBusyPlace(self):
        with self.assertRaises(LocationNotAvailable):
            self.game.move(self.ms_termi, (5, 5))

    def testHasMovedFlag(self):
        self.game.move(self.ms_termi, (4, 4))
        with self.assertRaises(HasMoved):
            self.game.move(self.ms_termi, (3, 3))

        self.game.new_round()
        # now the mage can move, but we need to update the object
        self.ms_termi = self.game.mages.get(id=self.ms_termi.id)
        self.game.move(self.ms_termi, (3, 3))


def CastingTestCase(TestCase):
    fixtures = ['test_fixtures.yaml']

    def setUp(self):
        m_termi = Mage.objects.get(name="Termifire")
        m_omega = Mage.objects.get(name="OmegaMax")
        p_toto = Player.objects.get(username="toto")
        p_titi = Player.objects.get(username="titi")
        self.ms_termi = MageInGame.from_mage(m_termi)
        self.ms_omega = MageInGame.from_mage(m_omega)

        self.ms_termi.use_deck(Deck.objects.get(name="deck de feu"))
        self.ms_omega.use_deck(Deck.objects.get(name="deck mouillé"))
        self.game = Game.new_game(
            player_1=p_toto,
            player_2=p_titi,
            mages_p1=[self.ms_termi,],
            mages_p2=[self.ms_omega,]
        )
        self.ms_termi.location = (4, 5)
        self.ms_termi.save()
