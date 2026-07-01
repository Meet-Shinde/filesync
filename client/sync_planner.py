from dataclasses import dataclass
from scanner import FileMetaData
from enum import Enum, auto
from change_detector import ChangeSet

class OperationType(Enum):
    UPLOAD = auto()
    DOWNLOAD = auto()
    DELETE = auto()

@dataclass
class Operation:
    type : OperationType
    file : FileMetaData

@dataclass
class Plan:
    operations : list[Operation]

def create_plan(changes: ChangeSet):
    plan = Plan()


def _create_operation(changes: ChangeSet):
    pass


