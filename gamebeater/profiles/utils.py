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

class GameOwnershipsByCompletionStatus():
    def __init__(self, completion_status, gameownership_list, game_total):
        self.completion_status = completion_status
        self.gameownership_list = gameownership_list
        try:
            self.completion_status_percentage = int(
                100.0 * (float(self.gameownership_list.count())/float(game_total))
            )
        except ZeroDivisionError:
            self.completion_status_percentage = 0

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)
