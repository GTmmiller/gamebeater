class CompletionStatus():
    NOT_STARTED = 'N'
    IN_PROGRESS = 'I'
    ON_HOLD = 'O'
    COMPLETE = 'C'

    CHOICES = (
        (NOT_STARTED, 'Not Started'),
        (IN_PROGRESS, 'In Progress'),
        (ON_HOLD, 'On Hold'),
        (COMPLETE, 'Complete'),
    )

class OwnershipStatus():
    WANTS = 'W'
    BORROWS = 'B'
    OWNES_PHYSICAL = 'P'
    OWNES_VIRTUAL = 'V'

    CHOICES = (
        (WANTS, 'Wants'),
        (BORROWS, 'Borrows'),
        (OWNES_PHYSICAL, 'Owns Physically'),
        (OWNES_VIRTUAL, 'Owns Virtually'),
    )

class ObjectsByStatus():
    def __init__(self, status, object_list, object_total):
        self.status = status
        self.object_list = object_list
        try:
            self.status_percentage = int(
                100.0 * (float(self.object_list.count())/float(object_total))
            )
        except ZeroDivisionError:
            self.status_percentage = 0

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

def get_all_objects_by_status(objects, status_class, object_by_status_method):
    objects_by_status_list = []
    object_total = objects.count()

    for status in status_class.CHOICES:
        objects_by_status_list.append(
            ObjectsByStatus(
                status=status[1],
                object_list=object_by_status_method(status[0]),
                object_total=object_total
            )
        )
    return tuple(objects_by_status_list)
