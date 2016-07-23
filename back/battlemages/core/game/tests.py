from django.test import TestCase
from battlemages.core.mages.models import Mage
from battlemages.core.players.models import Player
from .models import Game

class InitGameTestCase(TestCase):
    "tests about setting up and destroying the game"
    fixtures = ['test_fixtures.yaml']

    def testFixtures(self):
        m = Mage.objects.first()
        print(m.name)

    def testNewGame(self):
        termi = Mage.objects.get(name="Termifire")
        omega = Mage.objects.get(name="OmegaMax")
        toto = Player.objects.get(username="toto")
        titi = Player.objects.get(username="titi")
