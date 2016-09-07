from abc import ABCMeta


class NoOperationMappingException(Exception):
    """
    no mapping operation for operation type
    """


class OperationType:
    ADDED_AS_FRIEND = 4
    BLOCKED = 8


class Operation(metaclass=ABCMeta):
    def __init__(self, operation):
        self.revision = operation['revision']
        self.opType = operation['opType']
        self.mid = operation['params'][0]


class AddedAsFriendOperation(Operation):
    def __init__(self, operation):
        super().__init__(operation)


class BlockedOperation(Operation):
    def __init__(self, operation):
        super().__init__(operation)


class OperationMapper:
    OPERATION_MAPPING = {
        OperationType.ADDED_AS_FRIEND, AddedAsFriendOperation,
        OperationType.BLOCKED, BlockedOperation,
    }

    @classmethod
    def map(cls, operation):
        class_ = cls.OPERATION_MAPPING.get(operation['opType'])
        if not class_:
            raise NoOperationMappingException()

        return class_(operation)