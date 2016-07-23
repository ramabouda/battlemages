import random

from django.core.validators import MaxValueValidator
from django.db import models
from battlemages.core.mages.models import Mage
from battlemages.core.spells.models import Spell

from .constants import MANA_MAX, MAX_X, MAX_Y, TEAM_CHOICES
from .exceptions import HasMoved, HasCasted, NotInHand, CannotPay, IsDead

class Card(models.Model):
    spell = models.ForeignKey(Spell, related_name="cards")
    mage = models.ForeignKey('MageState')
    used = models.BooleanField(default=False)
    in_hand = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({}used)".format(self.spell, "" if self.used else "not ")

# decorator to easily ensure that a mage is not dead before performing an action
# see https://stackoverflow.com/questions/11731136/python-class-method-decorator-w-self-arguments
def not_if_dead(f):
    def wrapper(*args, **kwargs):
        if args[0].dead:  # args[0] is self
            raise IsDead
        return f(*args, **kwargs)
    return wrapper

class MageState(models.Model):
    mage = models.ForeignKey(Mage, on_delete=models.PROTECT)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='mages')
    team = models.PositiveSmallIntegerField(choices=TEAM_CHOICES)
    location_x = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_X)])
    location_y = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_Y)])
    hp = models.SmallIntegerField()
    mana = models.SmallIntegerField(default=0)
    dead = models.BooleanField(default=False)
    has_moved = models.BooleanField(default=False)
    has_casted = models.BooleanField(default=False)

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

    @not_if_dead
    def move(self, location):
        if self.has_moved:
            raise HasMoved("tried to move but found has_moved as True")
        self.location = location
        self.has_moved = True

    @not_if_dead
    def use_card(self, card, *args, **kwargs):
        "Validate the casting, pay the mana"
        if self.has_casted:
            raise HasCasted("tried to move but found has_casted as True")
        if not self.cards.filter(in_hand=True, id=card.id).exists():
            raise NotInHand
        if self.mana - card.spell.mana_cost < 0:
            raise CannotPay
        if self.has_casted:
            raise HasCasted("tried to cast but found has_casted as True")
        card.spell.cast(self, *args, **kwargs)
        # will not be affected if previous line raises an exception
        self.mana -= spell.mana_cost
        self.has_casted = True
        card.used = True
        card.save()

    @not_if_dead
    def draw_new_card(self):
        "place a random card in hand"
        try:
            card = random.choice(self.cards.filter(in_hand=False, used=False))
            card.in_hand = True
            card.save()
        except IndexError: # will be raised if no more cards are left to be used
            pass

    @not_if_dead
    def start_new_round(self):
        """reinit the state of the mage for a new round.
        
        Increase mana, draw new card, allow movement and casting."""
        self.has_moved = False
        self.has_casted = False
        self.mana = min(MANA_MAX, self.mana + MANA_REGEN)
        self.draw_next_card()
        # FIXME when should this check be exactly?
        if self.cards.filter(in_hand=False, used=False).count() == 0:
            self.die()

    def use_deck(self, deck):
        "helper function to convert a Deck to individual cards. To be used before a game"
        cards = []
        for e in deck.elements:
            for n in range(e.number):
                cards.append(Card(spell=e.spell, mage=self))
        Card.objects.bulk_create(cards)


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

    def use_card(self, attacker, card, *args, **kwargs):
        # TODO validate the spell
        attacker.use_card(card, *args, **kwargs)

    # FIXME is this still usefull?
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
