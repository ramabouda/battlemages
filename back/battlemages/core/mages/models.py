from django.db import models
from battlemages.core.spells.models import Spell
from battlemages.core.constants import ELEMENT_CHOICES


DEFAULT_HP_MAX = 15

class Mage(models.Model):
    name = models.CharField(max_length=32)
    hp_max = models.SmallIntegerField(default=DEFAULT_HP_MAX)
    spells = models.ManyToManyField(Spell)
    element = models.CharField(max_length=8, choices=ELEMENT_CHOICES)

    def __str__(self):
        return self.name
