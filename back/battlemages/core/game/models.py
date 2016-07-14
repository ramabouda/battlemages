from django.core.validators import MaxValueValidator
from django.db import models
from battlemages.core.mages.models import Mage
from battlemages.core.spells.models import Spell

from .constants import MANA_MAX, MAX_X, MAX_Y, TEAM_CHOICES

class MageState(models.Model):
    mage = models.ForeignKey(Mage, on_delete=models.PROTECT)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='mages')
    team = models.PositiveSmallIntegerField(
        choices=TEAM_CHOICES)
    location_x = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_X)])
    location_y = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_Y)])
    hp = models.SmallIntegerField()
    mana = models.SmallIntegerField(default=0)
    spells_in_hand = models.ManyToManyField(Spell, related_name="in_hand_of")
    discarded_spells = models.ManyToManyField(Spell, related_name="discarded_by")
    dead = models.BooleanField(default=False)
    can_move = models.BooleanField(default=True)
    can_cast = models.BooleanField(default=True)

    @property
    def location(self):
        return (self.location_x, self.location_y)

    @location.setter
    def location(self, new_location):
        self.location_x, self.location_y = new_location

    def _lose_hp(self, amount):
        if self.hp - amount < 0:
            self._die()
        else:
            self.hp -= amount

    def _die(self):
        "handle the consequences of death"
        self.dead = True

    def receive_damage(self, amount):
        self._lose_hp(amount)

    def move(self, location):
        assert self.can_move, "tried to move but found can_move as False"
        self.location = location
        self.can_move = False

    def cast_spell(self, spell):
        "Validate the casting, pay the mana"
        assert self.can_cast, "tried to cast a spell but found can_cast as False"
        self.mana -= spell.mana_cost
        self.can_cast = False

    def start_new_round(self):
        """reinit the state of the mage for a new round.
        
        Increase mana, allow movement and casting."""
        self.can_move = True
        self.can_cast = True
        self.mana = min(MANA_MAX, self.mana + MANA_REGEN)


class Game(models.Model):
    round_number = models.PositiveSmallIntegerField(default=0)

    def new_round(self):
        for ms in self.mages.all():
            ms.start_new_round()
        self.round_number += 1

    def move(self, mage, location):
        "Move the mage to the location given as a tuple (x, y)"
        # TODO validate the new location
        mage.move(location)

    def cast_spell(self, attacker, target, spell):
        # TODO validate the spell
        spell.cast(attacker=attacker, target=target)

    @classmethod
    def new_game(player_1, player_2, mages_p1, mages_p2):
        "Create a new game given the players and the lists of mages they are going to use"
        game = Game.objects.create()
        #TODO use bulk_create
        for mage in mages_p1:
            MageState.objects.create(
                mage=mage,
                game=game,
                team=TEAM_CHOICES[0][0],
                #TODO location
                location_x=5,
                location_y=5,
                hp=mage.hp_max,
                #TODO spells_in_hand
            )
        for mage in mages_p2:
            MageState.objects.create(
                mage=mage,
                game=game,
                team=TEAM_CHOICES[1][0],
                #TODO location
                location_x=5,
                location_y=5,
                hp=mage.hp_max,
                #TODO spells_in_hand
            )
        return game
