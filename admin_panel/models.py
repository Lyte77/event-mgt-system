

# myapp/models.py
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince

class ActivityLog(models.Model):
    # Restricts choices to the exact colors used in your CSS variables
    COLOR_CHOICES = [
        ('var(--amber)', 'Amber'),
        ('var(--green)', 'Green'),
        ('var(--blue)', 'Blue'),
        ('var(--brand)', 'Brand'),
        ('var(--red)', 'Red'),
    ]
    
    dot_color = models.CharField(max_length=30, choices=COLOR_CHOICES, default='var(--blue)')
    html_text = models.TextField(help_text="Stores pre-formatted HTML snippet for HTMX display")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']  # Newest items always appear at the top

    @property
    def human_time(self):
        """Converts database timestamp into clean short-hand strings like '2m ago' or '1h ago'"""
        now = timezone.now()
        if (now - self.created_at).total_seconds() < 60:
            return "Just now"
        
        # Pulls the primary timeframe interval segment
        delta_str = timesince(self.created_at, now).split(',')[0]
        
        # Clean formatting replacements to match your UI mockups
        replacements = [
            (' minutes', 'm'), (' minute', 'm'),
            (' hours', 'h'), (' hour', 'h'),
            (' days', 'd'), (' day', 'd'),
            (' weeks', 'w'), (' week', 'w')
        ]
        for old, new in replacements:
            delta_str = delta_str.replace(old, new)
        return f"{delta_str} ago"


class Collective(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name