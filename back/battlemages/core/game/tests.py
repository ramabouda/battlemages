from django.test import TestCase
from battlemages.core.mages.models import Mage
from battlemages.core.players.models import Player
from battlemages.core.spells.models import Deck
from .models import Game, MageInGame, Card

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
        ms_omega = MageInGame.from_mage(self.m_termi)

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

        # test cascading delete
        game.delete()
        self.assertFalse(Card.objects.exists())
        self.assertFalse(MageInGame.objects.exists())
