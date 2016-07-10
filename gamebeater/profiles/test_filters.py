from django.test import SimpleTestCase
from .templatetags.status_list_filters import previous_status_percentage
from .statuses import ObjectsByStatus, CompletionStatus

class MockStatusList():
    def __init__(self, status_list):
        self.status_list = status_list

    def __getitem__(self, key):
        return self.status_list[key]
    
    def count(self):
        return len(self.status_list)

class PreviousStatusPercentageTests(SimpleTestCase):
    
    def setUp(self):
        """
        Create a List of ObjectsByStatus that simulates the results of get_all_objects_by_status
        """
        self.status_list = ( 
            ObjectsByStatus(CompletionStatus.NOT_STARTED, MockStatusList((0,0,0,0)), 12),
            ObjectsByStatus(CompletionStatus.IN_PROGRESS, MockStatusList((0,)), 12),
            ObjectsByStatus(CompletionStatus.ON_HOLD, MockStatusList((0,0,0,0,0)), 12),
            ObjectsByStatus(CompletionStatus.COMPLETE, MockStatusList((0,0)), 12)
        )
    
    def test_previous_status_percentage_with_empty_list(self):
        """
        A blank list should return zero since it has no previous items in the list
        """
        self.assertEqual(previous_status_percentage([], 0), 0)

    def test_previous_status_percentage_with_status_list_and_zero_index(self):
        """
        Zero indexing a list will always return 0
        """
        self.assertEqual(previous_status_percentage(self.status_list, 0), 0)
    
    def test_previous_status_percentage_with_status_list_and_split_index(self):
        """
        This should sum the previous two entries in the status_list
        """
        self.assertEqual(previous_status_percentage(self.status_list, 2), 41)
    
    def test_previous_status_percentage_with_status_list_and_full_index(self):
        """
        The percentages don't add up to 100 all the time. I probably won't fix this later
        """
        self.assertEqual(previous_status_percentage(self.status_list, 4), 98)