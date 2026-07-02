from models import Change , ChangeSet , ChangeType , Operation , OperationType , Plan 

def create_plan(changes: ChangeSet):
    plan = Plan(
        operations = []
    )

    for change in changes.iter_changes():
        plan.operations.append(_create_operation(change))

    return plan

def _create_operation(change : Change):
    if change.change_type == ChangeType.ADDED:
        operation = Operation(
            type = OperationType.UPLOAD,
            file = change.new_metadata
        )
        return operation
    
    if change.change_type == ChangeType.DELETED:
        operation = Operation(
            type = OperationType.DELETE,
            file = change.old_metadata
        )
        return operation
    
    if change.change_type == ChangeType.MODIFIED:
        operation = Operation(
            type = OperationType.UPLOAD,
            file = change.new_metadata
        )
        return operation
