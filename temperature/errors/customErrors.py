class ServiceConnectionError(Exception):
    pass


class RessourceError(Exception):
    pass


class SerializerError(Exception):
    pass


class DuplicateStdnamesIdError(Exception):
    pass


class NoExcelFileError(Exception):
    pass


class InternalAssertionError(Exception):
    pass


class Non200RespError(Exception):
    pass


class NonSuccessRespError(Exception):
    pass


class InputLogicValidationError(Exception):
    pass


class HashException(Exception):
    pass

class DataNotAvailable(Exception):
    pass

class DataEmpty(Exception):
    pass

class TooFewChannels(Exception):
    pass

class MinLagLargerThanMaxLag(Exception):
    pass

class ArrayLengthError(Exception):
    pass

class BothChannelsNotFound(Exception):
    pass

class ChannelNotFound(Exception):
    pass

class StationsNotFound(Exception):
    pass