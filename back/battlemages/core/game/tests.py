from django.test import TestCase
from battlemages.core.mages.models import Mage
from .models import Game

class GameTestCase(TestCase):
    fixtures = ['test_fixtures.yaml']

    def testFixtures(self):
        m = Mage.objects.first()
        print(m.name)
