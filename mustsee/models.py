from django.db import models
from positions.fields import PositionField

class Attraction(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class UserRank(models.Model):
    attraction = models.ForeignKey(
        Attraction, related_name='ranks')
    session_uuid = models.CharField(max_length=32)
    rank = PositionField(collection='session_uuid', null=True)

    class Meta:
        unique_together = ('attraction', 'session_uuid')
