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
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    deck = models.ForeignKey('Deck', related_name="elements", on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('spell', 'deck')

    def __str__(self):
        return "{}*{}".format(self.number, self.spell)


class Deck(models.Model):
    name = models.CharField(max_length=50, default="New deck")

    def __str__(self):
        return self.name

    def add_spell(self, spell):
        try:
            element = self.elements.get(spell=spell)
            element.number += 1
            element.save()
        except DeckElement.DoesNotExist:
            DeckElement.objects.create(
                spell=spell,
                deck=self,
            )
