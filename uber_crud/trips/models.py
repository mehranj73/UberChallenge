from django.db import models



class Trip(models.Model):

    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"

    TRIP_STATUS = [
        (COMPLETED, "COMPLETED"),
        (IN_PROGRESS, "IN_PROGRESS"),
        (REQUESTED, "REQUESTED"),
        (ACCEPTED, "ACCEPTED")
    ]

    from_user = models.ForeignKey(
        'accounts.User',
        on_delete = models.CASCADE,
        related_name="customer"
    )

    status = models.CharField(
        choices=TRIP_STATUS,
        default=REQUESTED,
        max_length=20
    )

    driver = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="driver"
    )
    pickup_address = models.CharField(
        max_length=60,
        blank=True,
        default="BASIC PICK UP ADDRESS"
    )

    dropoff_address =models.CharField(
        max_length=60,
        blank=True,
        default="BASIC DROP OFF ADDRESS"
    )

    pickup_time = models.DateTimeField(blank=True, null=True)
    dropoff_time = models.DateTimeField(blank=True, null=True)
    accepted_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"requested a trip from {self.pickup_address} to {self.dropoff_address}"
