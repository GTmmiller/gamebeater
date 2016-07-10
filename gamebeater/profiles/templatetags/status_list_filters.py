from django import template

register = template.Library()

@register.filter
def previous_status_percentage(status_list, index):
    """
    Sums the status_percentage of the status in status_list before index.
    This is for finding the length of invisible progress bars in stat boxes
    """
    previous_percentage = 0
    for status in status_list[:index]:
        previous_percentage += status.status_percentage
    
    return previous_percentage