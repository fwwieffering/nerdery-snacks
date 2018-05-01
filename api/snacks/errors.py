
class UserAlreadyExistsException(Exception):
    pass


class VotesExceededException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class AuthorizationError(Exception):
    pass


class ApiNotAvailableException(Exception):
    pass


class BadRequestError(Exception):
    pass
