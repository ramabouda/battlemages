class HasMoved(Exception):
    pass

class HasCasted(Exception):
    pass

class NotInHand(Exception):
    pass

class CannotPay(Exception):
    pass

class IsDead(Exception):
    pass

class InvalidLocation(Exception):
    pass

class OutOfBoundaries(InvalidLocation):
    pass

class OutOfRange(InvalidLocation):
    pass

class LocationNotAvailable(InvalidLocation):
    pass
