from datetime import datetime

from django.db import models
from safedelete.models import SafeDeleteModel


class AbstractModel(SafeDeleteModel):
    """
    Abstract model containing fields which should be present in every model.
    Inherits from SafeDeleteModel so that nothing is hard deleted from the db.
    Every model should inherit it.
    """
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(AbstractModel, self).save(*args, **kwargs)


# Create your models here.
class Link(AbstractModel):
    original_url = models.URLField(null=True)
    tiny_id = models.URLField(null=True)
    total_hits = models.IntegerField(default=0)

    def get_link_id(self):
        from .helpers import index_to_char

        _id = self.id
        digits = []
        while _id > 0:
            rem = _id % 62
            digits.append(rem)
            _id /= 62
        digits.reverse()
        return index_to_char(digits)

    @property
    def hourly_hits(self):
        then, now = self.added_on, datetime.now()
        diff = now - then
        diff_hours = diff.seconds / 3600
        return self.total_hits/diff_hours

    @staticmethod
    def decode_id(string):
        from .helpers import _char_map
        i = 0
        for c in string:
            i = i * 64 + _char_map.index(c)
        return i
