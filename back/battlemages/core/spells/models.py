from django.db import models
from battlemages.core.constants import ELEMENT_CHOICES


class Spell(models.Model):
    name = models.CharField(max_length=32)
    # contains db_index=True
    slug = models.SlugField(max_length=32)
    mana_cost = models.SmallIntegerField(default=0)
    damage = models.SmallIntegerField(default=0)
    mana_damage = models.SmallIntegerField(default=0)
    element = models.CharField(max_length=8, choices=ELEMENT_CHOICES)

    def __str__(self):
        return self.name

    def cast(self, attacker, *, target=None):
        attacker.cast_spell(self)
        if target is not None:
            target.receive_damage(self.damage)


class DeckElement(models.Model):
    spell = models.ForeignKey(Spell)
    deck = models.ForeignKey('Deck')
    number = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('spell', 'deck')


class Deck(models.Model):
    name = models.CharField(max_length=50, default="New deck")
    cards = models.ManyToManyField(Spell, through=DeckElement)

    def __str__(self):
        return self.name
