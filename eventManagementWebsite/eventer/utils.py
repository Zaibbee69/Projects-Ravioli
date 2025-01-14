from django.core.paginator import Paginator
from django.template.defaultfilters import truncatewords



# Function to paginate my events 
def paginator_six_thousand(post, page_number):

    # First paginating the posts to a set number
    paginator = Paginator(post, 6)

    # Now returning the paginated posts depending upon the page number
    paginated_posts = paginator.get_page(page_number)

    # Return data
    return paginated_posts


def truncator_six_thousand(events):

    processed_events = []
    for event in events:
        truncated_description = truncatewords(event.description, 10)
        event.truncated = len(event.description.split()) > 10
        event.truncated_description = truncated_description
        processed_events.append(event)

    return processed_events
