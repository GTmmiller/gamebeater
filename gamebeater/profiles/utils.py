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
