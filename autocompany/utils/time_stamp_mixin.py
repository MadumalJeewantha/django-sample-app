from django.db import models


class TimeStampMixin(models.Model):
    """
    Include created and updated timestamp.
    auto_now_add will set the timezone.now() only when the instance is created,
    and auto_now will update the field everytime the save method is called.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
