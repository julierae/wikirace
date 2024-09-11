from django.db import models

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/"


class Race(models.Model):
    start_title = models.CharField(max_length=255)
    end_title = models.CharField(max_length=255)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.start_title} to {self.end_title}"

    def get_start_url(self):
        return f"{WIKIPEDIA_URL}{self.start_title}"

    def get_end_url(self):
        return f"{WIKIPEDIA_URL}{self.end_title}"

    def get_elapsed_time(self):
        if self.start_at and self.end_at:
            return self.end_at - self.start_at
        return None

    get_elapsed_time.short_description = "Elapsed Time"

    def get_elapsed_time_str(self):
        elapsed_time = self.get_elapsed_time()
        if elapsed_time:
            return f"{elapsed_time.total_seconds()} seconds"

    get_elapsed_time_str.short_description = "Seconds Elapsed"
