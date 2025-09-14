from django.db import models

from django.utils.timezone import now


class TicketManager(models.Manager):
    def for_user(self, user):
        """All tickets for a given user"""
        return self.filter(user=user)
    
    
    def upcoming_for_user(self, user):
        """Future events only"""
        return self.for_user(user).filter(event__start_time__gte=now()).order_by("event__start_time")

    def past_for_user(self, user):
        """Past events only"""
        return self.for_user(user).filter(event__start_time__lt=now()).order_by("-event__start_time")

    def paid_for_user(self, user):
        """Paid tickets only"""
        return self.for_user(user).filter(payment_status="paid")

    def pending_for_user(self, user):
        """Pending tickets only"""
        return self.for_user(user).filter(payment_status="pending")

    def refunded_for_user(self, user):
        """Refunded tickets only"""
        return self.for_user(user).filter(payment_status="refunded")