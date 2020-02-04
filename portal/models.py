from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Building(models.Model):
    """Has the buildings which are to be populated."""

    name = models.CharField(max_length=128, db_index=True, unique=True)
    occupancy = models.IntegerField(default=800, null=False,)
    # current_waitlist_done = models.IntegerField(default=0,)
    # placed = models.IntegerField(default=0,)

    class Meta:
        verbose_name = "building"
        verbose_name_plural = "buildings"

    def __str__(self):
        return self.name


class Queuer(models.Model):
    """People who are currently in queue."""

    date_applied = models.DateField(auto_now_add=True,)

    building_applied = models.ForeignKey("Building", on_delete=models.PROTECT)
    placed = models.BooleanField(null=False, default=False)
    name = models.CharField(max_length=126,)
    email = models.EmailField(max_length=254)
    roll_number = models.CharField(max_length=10)
    contact_number = PhoneNumberField(default="",)
    spouse_name = models.CharField(max_length=126,)
    waitlist_number = models.IntegerField(default=0, db_index=True)

    marriage_certificate_verified = models.BooleanField(null=False, default=False)
    aadhaar_card_verified = models.BooleanField(null=False, default=False)
    spouse_aadhaar_card_verified = models.BooleanField(null=False, default=False)
    institute_ID_verified = models.BooleanField(null=False, default=False)

    marriage_certificate = models.FileField(upload_to="marriage_certi/",)
    your_aadhaar_card = models.FileField(upload_to="your_aadhaar_card/",)
    spouse_aadhaar_card = models.FileField(upload_to="spouse_aadhaar_card/",)

    # At any point of time:
    #   people living in building = count(placed=True, building_applied)
    #   waitlist_number = count(Queuer) - count(placed=True)

    class Meta:
        verbose_name = "queuer"
        verbose_name_plural = "queuers"
        unique_together = ("building_applied", "waitlist_number")
        unique_together = ("name", "roll_number", "building_applied")

    def __str__(self):
        return self.name

    def current_waitlist(self):
        if not (
            self.marriage_certificate_verified
            and self.aadhaar_card_verified
            and self.spouse_aadhaar_card_verified
            and self.institute_ID_verified
        ):
            return "N/A"
        if self.placed is True:
            return 0
        return Queuer.objects.filter(
            building_applied=self.building_applied,
            placed=False,
            waitlist_number__range=(0, self.waitlist_number),
            marriage_certificate_verified=True,
            aadhaar_card_verified=True,
            spouse_aadhaar_card_verified=True,
            institute_ID_verified=True,
        ).count()

    def save(self):
        queuer = Queuer.objects.filter(id=self.id)
        if not queuer:
            self.waitlist_number = (
                Queuer.objects.filter(
                    building_applied=self.building_applied, placed=False
                ).count()
                + 1
            )

        super(Queuer, self).save()
