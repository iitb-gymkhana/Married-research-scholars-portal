from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import logging
logger = logging.getLogger('__name__')
from django.core.mail import send_mail



# class Building(models.Model):
#     """Has the buildings which are to be populated."""

#     name = models.CharField(max_length=128, db_index=True, unique=True)
#     occupancy = models.IntegerField(default=800, null=False, )

#     # queuer = models.ForeignKey("Queuer", on_delete=models.CASCADE, null=True)
#     # current_waitlist_done = models.IntegerField(default=0,)
#     # placed = models.IntegerField(default=0,)

#     class Meta:
#         verbose_name = "building"
#         verbose_name_plural = "buildings"

#     def __str__(self):
#         return self.name


# class Queuer(models.Model):
#     """People who are currently in queue."""

#     date_applied = models.DateTimeField(
#         null=False, default=timezone.now, editable=False
#     )

#     building = models.ForeignKey("Building", on_delete=models.PROTECT, null=True)
#     placed = models.BooleanField(null=False, default=False)
#     room_number_if_placed = models.CharField(max_length=6, null=True, blank=True)

#     name = models.CharField(max_length=126, )
#     email = models.EmailField(max_length=254)
#     roll_number = models.CharField(max_length=10)
#     # date_of_registration = models.DateField(null=False)
#     # date_of_marriage = models.DateField(null=False)
#     contact_number = PhoneNumberField(default="", )
#     # permanent_address = models.TextField(null=False)
#     scholarship = models.CharField(max_length=128, choices=[
#         ('I', "Institute"),
#         ('CSIR', 'CSIR'),
#         ('UGC', 'UGC'),
#         ('None', 'None')
#     ],
#                                    null=False,
#                                    default="None")
#     scholarship_start_date = models.DateField(null=True)
#     spouse_name = models.CharField(max_length=126, )
#     # waitlist_number = models.IntegerField(default=0, db_index=True, editable=False)
#     waitlist_Type1 = models.IntegerField(default=0, db_index=True, editable=False)
#     waitlist_Tulsi = models.IntegerField(default=0, db_index=True, editable=False)
#     waitlist_MRSB = models.IntegerField(default=0, db_index=True, editable=False)

#     # type1 = models.ForeignKey("Building", related_name="Type1",on_delete=models.PROTECT, null=True)
#     # tulsi = models.ForeignKey("Building", related_name="Tulsi", on_delete=models.PROTECT, null=True)
#     # mrsb = models.ForeignKey("Building", related_name="MRSB", on_delete=models.PROTECT, null=True)

#     marriage_certificate_verified = models.BooleanField(null=False, default=False)
#     aadhaar_card_verified = models.BooleanField(null=False, default=False)
#     spouse_aadhaar_card_verified = models.BooleanField(null=False, default=False)
#     institute_ID_verified = models.BooleanField(null=False, default=False)

#     verified_time = models.DateTimeField(null=True, blank=True)

#     marriage_certificate = models.FileField(upload_to="marriage_certi/", )
#     your_aadhaar_card = models.FileField(upload_to="your_aadhaar_card/", )
#     spouse_aadhaar_card = models.FileField(upload_to="spouse_aadhaar_card/", )

#     # dependant = models.ForeignKey(Dependant, on_delete=models.CASCADE, null=True)
#     # At any point of time:
#     #   people living in building = count(placed=True, building_applied)
#     #   waitlist_number = count(Queuer) - count(placed=True)

#     class Meta:
#         verbose_name = "queuer"
#         verbose_name_plural = "queuers"
#         unique_together = ("name", "roll_number", "building")
#         unique_together = ("roll_number", "building")

#     def __str__(self):
#         return self.name

#     def all_verified(self):
#         # returns if everything is verified or not
#         return bool(
#             self.marriage_certificate_verified
#             and self.aadhaar_card_verified
#             and self.spouse_aadhaar_card_verified
#             and self.institute_ID_verified
#         )

#     all_verified.boolean = True  # For bool on admin page

#     def current_waitlist(self):
#         if not self.all_verified():
#             return "N/A"
#         if self.placed is True:
#             return 0

#         initDateTime = Queuer.objects.earliest("date_applied").date_applied
#         sort_verified_time = Queuer.objects.filter(
#             # building_applied=self.building_applied,
#             placed=False,
#             verified_time__range=[initDateTime, self.verified_time],
#             marriage_certificate_verified=True,
#             aadhaar_card_verified=True,
#             spouse_aadhaar_card_verified=True,
#             institute_ID_verified=True,
#         ).count()

#         if sort_verified_time == 0:
#             # In case algorithm fails.
#             return "Check Manually"

#         else:
#             return sort_verified_time

#     def save(self):
#         # Handle initial cases of converting date into date time
#         if not self.date_applied:
#             self.date_applied = timezone.now()
#             if self.all_verified():
#                 self.verified_time = timezone.now()

#         if not self.id:
#             # self.waitlist_number = (
#             #     Queuer.objects.filter(
#             #         # building_applied=self.building_applied,
#             #         placed=False
#             #     ).count()
#             #     + 1
#             # )
#             self.waitlist_Type1 = (
#                     Queuer.objects.filter(
#                         building__name__contains="Type",
#                         placed=False
#                     ).count()
#                     + 1
#             )
#             self.waitlist_Tulsi = (
#                     Queuer.objects.filter(
#                         building__name__contains="Tulsi",
#                         placed=False
#                     ).count()
#                     + 1
#             )
#             self.waitlist_MRSB = (
#                     Queuer.objects.filter(
#                         building__name__contains="Type",
#                         placed=False
#                     ).count()
#                     + 1
#             )
#             self.date_applied = timezone.now()

#         if not self.verified_time:
#             if self.all_verified():
#                 self.verified_time = timezone.now()

#         if not self.all_verified():
#             """ If an option is unchecked later, again remove the verified time """
#             self.verified_time = None

#         if self.room_number_if_placed:
#             # if entered room number, candidate is placed.
#             self.placed = True
#             # self.building_applied.occupancy -= 1
#             # print(self.building_applied.occupancy)
#             # self.building_applied.save()
#         else:
#             self.placed = False

#         super(Queuer, self).save()


# class Dependant(models.Model):
#     """A person belonging to the family of the applicant"""
#     # queuer = models.ForeignKey(Queuer, on_delete=models.CASCADE)
#     name = models.CharField(max_length=126, null=False)
#     contact_number = PhoneNumberField(default="", blank=True)
#     photo = models.FileField(upload_to="dependants/", blank=True)
#     relation = models.CharField(max_length=128, choices=[
#         ("F", 'Father'),
#         ('M', 'Mother'),
#         ('FIL', 'Father-in-Law'),
#         ('MIL', 'Mother-in-Law'),
#         ('C', 'Child')
#     ], null=True)
#     queuer = models.ForeignKey(Queuer, on_delete=models.CASCADE, null=True)

#     class Meta:
#         verbose_name = "Dependant"
#         verbose_name_plural = "Dependants"

#     def __str__(self):
#         return self.queuer.name + '_' + self.relation


class Applicant(models.Model):
    name = models.CharField(max_length=128)
    roll_number = models.CharField(max_length=128)
    date_of_registration = models.DateField(null=False)
    department = models.CharField(max_length=128, help_text="For example, 'Energy Science and Engineering'", null=False)
    date_of_marriage = models.DateField(null=True, default='', blank=False)
    email = models.EmailField(max_length=256)
    phone_number = PhoneNumberField(default='')
    permanent_address = models.TextField(default='', null=False)
    scholarship = models.CharField(max_length=128, choices=[
        ('I', 'Institute'),
        ('CSIR', 'CSIR'),
        ('UGC', 'UGC')
    ], null=True)
    date_of_scholarship = models.DateField(null=True, default='')
    course_work_completed_on = models.DateField(null=True, default='', help_text='Give the expected date')
    course_work_completed_by = models.CharField(max_length=128)
    marriage_certificate = models.FileField(upload_to='marriage_certificates/', null=True, blank=False)
    joint_photograph_with_spouse = models.FileField(upload_to='photo_with_spouse/', null=True, blank=False)
    coursework_grade_sheet = models.FileField(upload_to='grade_sheet/', null=True, blank=False)
    recommendation_of_guide_for_accomodation = models.FileField(upload_to='guide_recommendation/', null=True,
                                                                blank=False)
    spouse_name = models.CharField(max_length=128, null=True, blank=False, default='Spouse')
    spouse_roll_number = models.CharField(max_length=128, null=True, blank=False, default='N/A')
    spouse_designation = models.CharField(max_length=128, null=True, blank=False, default='N/A')
    marriage_certificate_verified = models.BooleanField(default=False, null=False)
    joint_photograph_with_spouse_verified = models.BooleanField(default=False, null=False)
    coursework_grade_sheet_verified = models.BooleanField(default=False, null=False)
    recommendation_of_guide_for_accomodation_verified = models.BooleanField(default=False, null=False)
    feedback = models.TextField(default='Your Documents are not yet verified!', null=True, blank=True)
    waitlist_Type1 = models.IntegerField(default='0', db_index=True, editable=False)
    waitlist_Tulsi = models.IntegerField(default=0, db_index=True, editable=False)
    waitlist_MRSB = models.IntegerField(default=0, db_index=True, editable=False)
    date_applied = models.DateTimeField(null=False, default=timezone.now, editable=False)
    verified_time = models.DateTimeField(null=True, blank=True)
    occupied_Type1 = models.BooleanField(default=False)
    occupied_Tulsi = models.BooleanField(default=False)
    occupied_MRSB = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
        unique_together = ('name', 'roll_number')

    def __str__(self):
        return self.name

    def all_verified(self):
        return bool(self.marriage_certificate_verified and
                    self.coursework_grade_sheet_verified and
                    self.joint_photograph_with_spouse_verified and
                    self.recommendation_of_guide_for_accomodation_verified
                    )
    all_verified.boolean = True

    def save(self, flag=True, *args, **kwargs):
        if not self.id:
            if not self.date_applied:
                self.date_applied = timezone.now()
            # if self.all_verified():
            #     self.verified_time = timezone.now()
            # if self.all_verified():
            #     self.waitlist_Type1 = 1 + len(Applicant.objects.filter(
            #         occupied_Type1=False,
            #         marriage_certificate_verified=True,
            #         joint_photograph_with_spouse_verified=True,
            #         coursework_grade_sheet_verified=True,
            #         recommendation_of_guide_for_accomodation_verified=True,
            #         # building__name__contains='Type',
            #     ))
            #     self.waitlist_Tulsi = 1 + len(Applicant.objects.filter(
            #         occupied_Tulsi=False,
            #         marriage_certificate_verified=True,
            #         joint_photograph_with_spouse_verified=True,
            #         coursework_grade_sheet_verified=True,
            #         recommendation_of_guide_for_accomodation_verified=True
            #         # building__name__contains='Tulsi',
            #     ))
            #     self.waitlist_MRSB = 1 + len(Applicant.objects.filter(
            #         occupied_MRSB=False,
            #         marriage_certificate_verified=True,
            #         joint_photograph_with_spouse_verified=True,
            #         coursework_grade_sheet_verified=True,
            #         recommendation_of_guide_for_accomodation_verified=True
            #         # building__name__contains='MRSB',
            #     ))

                # if self.occupied_MRSB and not self.occupied_Tulsi and not self.occupied_Type1:
                #     self.waitlist_MRSB = 0
                # elif self.occupied_Tulsi and not (self.occupied_MRSB or self.occupied_Type1):
                #     self.waitlist_Tulsi = 0
                # elif self.occupied_Type1 and not (self.occupied_MRSB or self.occupied_Tulsi):
                #     self.waitlist_Type1 = 0
                # if self.occupied_MRSB or self.occupied_Tulsi or self.occupied_Type1:
                #     self.waitlist_Type1 = 0
                #     self.waitlist_Tulsi = 0
                #     self.waitlist_MRSB = 0
                #     for applicant in Applicant.objects.all():
                #         if applicant.name != self.name and applicant.roll_number != self.roll_number:
                #             print(applicant.name)
                #             applicant.waitlist_MRSB -= 1
                #             applicant.waitlist_Tulsi -= 1
                #             applicant.waitlist_Type1 -= 1
                #             applicant.save()

            
        else:
            if not self.verified_time:
                if self.all_verified():
                    self.verified_time = timezone.now()

            if not self.all_verified():
                """ If an option is unchecked later, again remove the verified time """
                self.verified_time = None
            
            if self.all_verified() and not (self.occupied_MRSB or self.occupied_Tulsi or self.occupied_Type1):
                if flag:
                    self.waitlist_Type1 = 1 + len(Applicant.objects.filter(
                        occupied_Type1=False,
                        marriage_certificate_verified=True,
                        joint_photograph_with_spouse_verified=True,
                        coursework_grade_sheet_verified=True,
                        recommendation_of_guide_for_accomodation_verified=True,
                    ))
                    self.waitlist_Tulsi = 1 + len(Applicant.objects.filter(
                        occupied_Tulsi=False,
                        marriage_certificate_verified=True,
                        joint_photograph_with_spouse_verified=True,
                        coursework_grade_sheet_verified=True,
                        recommendation_of_guide_for_accomodation_verified=True
                    ))
                    self.waitlist_MRSB = 1 + len(Applicant.objects.filter(
                        occupied_MRSB=False,
                        marriage_certificate_verified=True,
                        joint_photograph_with_spouse_verified=True,
                        coursework_grade_sheet_verified=True,
                        recommendation_of_guide_for_accomodation_verified=True
                    ))
                else:
                    logger.error("Came Here!!")
                    pass

            elif self.all_verified() and (self.occupied_MRSB or self.occupied_Tulsi or self.occupied_Type1):
                if self.occupied_Type1:
                    for applicant in Applicant.objects.filter(marriage_certificate_verified=True,
                                                              joint_photograph_with_spouse_verified=True,
                                                              coursework_grade_sheet_verified=True,
                                                              recommendation_of_guide_for_accomodation_verified=True,
                                                              occupied_Type1=False):
                        if applicant.name != self.name:
                            if applicant.waitlist_Type1 > self.waitlist_Type1:
                                applicant.waitlist_Type1 -= 1
                                applicant.save(flag=False)
                    self.waitlist_Type1 = 0
                    # send confirmation email
                elif self.occupied_Tulsi:
                    for applicant in Applicant.objects.filter(marriage_certificate_verified=True,
                                                              joint_photograph_with_spouse_verified=True,
                                                              coursework_grade_sheet_verified=True,
                                                              recommendation_of_guide_for_accomodation_verified=True,
                                                              occupied_Tulsi=False):
                        if applicant.name != self.name:
                            if applicant.waitlist_Tulsi > self.waitlist_Tulsi:
                                applicant.waitlist_Tulsi -= 1
                                applicant.save(flag=False)
                    self.waitlist_Tulsi = 0
                    # send confirmation email
                elif self.occupied_MRSB:
                    for applicant in Applicant.objects.filter(marriage_certificate_verified=True,
                                                              joint_photograph_with_spouse_verified=True,
                                                              coursework_grade_sheet_verified=True,
                                                              recommendation_of_guide_for_accomodation_verified=True,
                                                              occupied_MRSB=False):
                        if applicant.name != self.name:
                            if applicant.waitlist_MRSB > self.waitlist_MRSB:
                                applicant.waitlist_MRSB -= 1
                                applicant.save(flag=False)
                    self.waitlist_MRSB = 0
                    # send confirmation email
            # else:
            #     self.waitlist_MRSB = 0
            #     self.waitlist_Tulsi = 0
            #     self.waitlist_Type1 = 0
            
        super(Applicant, self).save(*args, **kwargs)
