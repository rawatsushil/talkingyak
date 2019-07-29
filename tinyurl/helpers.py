import string

from .models import Link


_char_map = string.ascii_letters+string.digits


def index_to_char(sequence):
    return "".join([_char_map[int(x)] for x in sequence])


def get_tiny_url(request, original_url):
    """
    check if the tiny url already exists then returns the same else creates new
    """
    url = is_tiny_url_exists(original_url)
    if url:
        return request.build_absolute_uri(url)
    return create_tiny_url(request, original_url)


def create_tiny_url(request, url):
    """
    Tiny url is created based on the id of the original link in db
    """
    link = Link(original_url=url)
    link.save()
    link.tiny_id = link.get_link_id()
    link.save()
    return request.build_absolute_uri(link.tiny_id)


def is_tiny_url_exists(url):
    data = Link.objects.filter(original_url=url)
    if data.exists():
        return data.first().tiny_id
