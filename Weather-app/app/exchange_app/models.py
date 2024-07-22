from django.db import models


class SearchHistory(models.Model):
    session_key = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'

    def __str__(self):
        return f"Search for {self.city} on {self.timestamp}"
