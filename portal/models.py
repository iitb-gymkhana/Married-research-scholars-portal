from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import logging
logger = logging.getLogger('__name__')
from django.core.mail import send_mail
from django.db.models import F


class Applicant(models.Model):
    name = models.CharField(max_length=128)
    roll_number = models.CharField(max_length=128)
    date_of_registration = models.DateField(null=False)
    department = models.CharField(max_length=128, help_text="For example, 'Electrical Engineering'", null=False)
    # date_of_marriage = models.DateField(null=True, default='', blank=False)
    email = models.EmailField(max_length=256)
    phone_number = PhoneNumberField(default='')
    permanent_address = models.TextField(default='', null=False)
    scholarship = models.CharField(max_length=128, choices=[
        ('I', 'Institute'),
        ('CSIR', 'CSIR'),
        ('UGC', 'UGC')
    ], null=True, verbose_name="Scholarship: Institute / CSIR / UGC")
    date_of_scholarship = models.DateField(null=True, default='', verbose_name="Date from which scholarship is awarded")
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
    waitlist_Type1 = models.IntegerField(default=0, db_index=True, editable=False)
    waitlist_Tulsi = models.IntegerField(default=0, db_index=True, editable=False)
    waitlist_MRSB = models.IntegerField(default=0, db_index=True, editable=False)
    date_applied = models.DateTimeField(null=False, default=timezone.now, editable=False, verbose_name="Date Applied")
    verified_time = models.DateTimeField(null=True, blank=True, verbose_name="Date of verification by HCU")
    occupied_Type1 = models.BooleanField(default=False)
    occupied_Tulsi = models.BooleanField(default=False)
    occupied_MRSB = models.BooleanField(default=False)
    defer_Type1 = models.BooleanField(default=False)
    defer_Tulsi = models.BooleanField(default=False)
    defer_MRSB = models.BooleanField(default=False)
    scholarship_awarded_upto = models.DateField(verbose_name="Initially the scholarship awarded up to", null=True, blank=True)
    acad_details_verified = models.BooleanField(default=False, verbose_name="The academic details are verified and found correct")
    acad_details_verification_date = models.DateTimeField(default=timezone.now, verbose_name="Verification Date by Academic Section", null=True)
    application_received_by_hcu_date = models.DateTimeField(verbose_name="Application Received by H.C.Unit Date:", null=True, blank=True)

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

    def occupied_any(self):
        return self.occupied_Type1 or self.occupied_Tulsi or self.occupied_MRSB
    
    def deferred_any(self):
        return self.defer_Type1 or self.defer_Tulsi or self.defer_MRSB

    def save(self, flag=True, *args, **kwargs):
        """
        flag is for dealing with occupy/vacate.
        flag = True when the applicant is getting added to the waitlist in the first place
        flag = False when the applicant is occupying or vacating or deferring the accomodation
        
        """
        if not self.id:
            if not self.date_applied:
                self.date_applied = timezone.now()
        else:
            if self.acad_details_verified:
                """If the academic details are successfully verified by Acad Office"""
                self.application_received_by_hcu_date = self.acad_details_verification_date
                if self.all_verified():
                    """If the marital details are successfully verified by HCU"""
                    self.verified_time = timezone.now()
                    qs = Applicant.objects.all().filter(acad_details_verified=True, marriage_certificate_verified=True,
                                                        joint_photograph_with_spouse_verified=True,
                                                        coursework_grade_sheet_verified=True,
                                                        recommendation_of_guide_for_accomodation_verified=True).order_by('date_applied')
                    if not self.occupied_any() and not self.deferred_any():
                        """Either entering into waitlist ot vacating the accomodation"""
                        if flag:
                            """Enter into waitlist"""
                            # qs = Applicant.objects.all().filter(acad_details_verified=True, marriage_certificate_verified=True,
                            #                               joint_photograph_with_spouse_verified=True,
                            #                               coursework_grade_sheet_verified=True,
                            #                               recommendation_of_guide_for_accomodation_verified=True).order_by('date_applied')
                            self.waitlist_Type1 = 1 + len(qs.filter(waitlist_Type1__gt=0, occupied_Type1=False))
                            self.waitlist_Tulsi = 1 + len(qs.filter(waitlist_Tulsi__gt=0, occupied_Tulsi=False))
                            self.waitlist_MRSB = 1 + len(qs.filter(waitlist_MRSB__gt=0, occupied_MRSB=False))
                        else:
                            """If the applicant has vacated"""
                            if not self.occupied_Tulsi:
                                self.waitlist_Tulsi = 0
                            elif not self.occupied_Type1:
                                self.waitlist_Type1 = 0
                            elif not self.occupied_MRSB:
                                self.waitlist_MRSB = 0
                            else:
                                pass
                    elif self.occupied_any() and not self.deferred_any():
                        """If the applicant has occupied any building"""
                        if self.occupied_Type1:
                            qs_excluded = qs.exclude(id=self.id, waitlist_Type1__lt=0) # exclude the current applicant and all those who are already occupying
                            qs_excluded = qs_excluded.exclude(waitlist_Type1__lt=self.waitlist_Type1)
                            qs_excluded.update(waitlist_Type1 = F('waitlist_Type1') - 1) # decrease the waitlist number by 1 for all those in the waitlist
                            self.waitlist_Type1 = -2
                        elif self.occupied_Tulsi:
                            qs_excluded = qs.exclude(id=self.id, waitlist_Tulsi__lt=0)  # exclude the current applicant and all those who are already occupying
                            qs_excluded = qs_excluded.exclude(waitlist_Tulsi__lt=self.waitlist_Tulsi)
                            qs_excluded.update(waitlist_Tulsi=F('waitlist_Tulsi') - 1)  # decrease the waitlist number by 1 for all those in the waitlist
                            self.waitlist_Tulsi = -2
                        elif self.occupied_MRSB:
                            qs_excluded = qs.exclude(id=self.id, waitlist_MRSB__lt=0)  # exclude the current applicant and all those who are already occupying
                            qs_excluded = qs_excluded.exclude(waitlist_MRSB__lt=self.waitlist_MRSB)
                            qs_excluded.update(waitlist_MRSB=F('waitlist_MRSB') - 1)  # decrease the waitlist number by 1 for all those in the waitlist
                            self.waitlist_Tulsi = -2
                        else:
                            pass
                        pass
                    elif not self.occupied_any() and self.deferred_any():
                        if self.defer_Type1:
                            self.waitlist_Type1 = -1
                        elif self.defer_Tulsi:
                            self.waitlist_Tulsi = -1
                        elif self.defer_MRSB:
                            self.waitlist_MRSB = -1
                    else:
                        pass
                else:
                    """If the all details are not verified by HCU"""
                    self.verified_time = None
            else:
                pass
            
            # if not self.verified_time:
            #     if self.all_verified():
            #         self.verified_time = timezone.now()

            # if not self.all_verified():
            #     """ If an option is unchecked later, again remove the verified time """
            #     self.verified_time = None
            
            # if self.all_verified() and not (self.occupied_MRSB or self.occupied_Tulsi or self.occupied_Type1):
            #     if flag:
            #         self.waitlist_Type1 = 1 + len(Applicant.objects.filter(
            #             occupied_Type1=False,
            #             marriage_certificate_verified=True,
            #             joint_photograph_with_spouse_verified=True,
            #             coursework_grade_sheet_verified=True,
            #             recommendation_of_guide_for_accomodation_verified=True,
            #         ))
            #         self.waitlist_Tulsi = 1 + len(Applicant.objects.filter(
            #             occupied_Tulsi=False,
            #             marriage_certificate_verified=True,
            #             joint_photograph_with_spouse_verified=True,
            #             coursework_grade_sheet_verified=True,
            #             recommendation_of_guide_for_accomodation_verified=True
            #         ))
            #         self.waitlist_MRSB = 1 + len(Applicant.objects.filter(
            #             occupied_MRSB=False,
            #             marriage_certificate_verified=True,
            #             joint_photograph_with_spouse_verified=True,
            #             coursework_grade_sheet_verified=True,
            #             recommendation_of_guide_for_accomodation_verified=True
            #         ))
            #     else:
            #         logger.error("Came Here!!")
            #         pass

            # elif self.all_verified() and (self.occupied_MRSB or self.occupied_Tulsi or self.occupied_Type1):
            #     if self.occupied_Type1:
            #         for applicant in Applicant.objects.filter(marriage_certificate_verified=True,
            #                                                   joint_photograph_with_spouse_verified=True,
            #                                                   coursework_grade_sheet_verified=True,
            #                                                   recommendation_of_guide_for_accomodation_verified=True,
            #                                                   occupied_Type1=False):
            #             if applicant.name != self.name:
            #                 if applicant.waitlist_Type1 > self.waitlist_Type1:
            #                     applicant.waitlist_Type1 -= 1
            #                     applicant.save(flag=False)
            #         self.waitlist_Type1 = 0
            #         self.defer_Type1 = False
            #         # send confirmation email
            #     elif self.occupied_Tulsi:
            #         for applicant in Applicant.objects.filter(marriage_certificate_verified=True,
            #                                                   joint_photograph_with_spouse_verified=True,
            #                                                   coursework_grade_sheet_verified=True,
            #                                                   recommendation_of_guide_for_accomodation_verified=True,
            #                                                   occupied_Tulsi=False):
            #             if applicant.name != self.name:
            #                 if applicant.waitlist_Tulsi > self.waitlist_Tulsi:
            #                     applicant.waitlist_Tulsi -= 1
            #                     applicant.save(flag=False)
            #         self.waitlist_Tulsi = 0
            #         self.defer_Tulsi = False
            #         # send confirmation email
            #     elif self.occupied_MRSB:
            #         for applicant in Applicant.objects.filter(marriage_certificate_verified=True,
            #                                                   joint_photograph_with_spouse_verified=True,
            #                                                   coursework_grade_sheet_verified=True,
            #                                                   recommendation_of_guide_for_accomodation_verified=True,
            #                                                   occupied_MRSB=False):
            #             if applicant.name != self.name:
            #                 if applicant.waitlist_MRSB > self.waitlist_MRSB:
            #                     applicant.waitlist_MRSB -= 1
            #                     applicant.save(flag=False)
            #         self.waitlist_MRSB = 0
            #         self.defer_MRSB = False
            #         # send confirmation email
            # # else:
            # #     self.waitlist_MRSB = 0
            # #     self.waitlist_Tulsi = 0
            # #     self.waitlist_Type1 = 0
            
        super(Applicant, self).save(*args, **kwargs)

# class Documents(models.Model):
#     applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE, primary_key=True)

#     spouse_name = models.CharField(max_length=128, null=True, blank=False, default='Spouse')
#     spouse_roll_number = models.CharField(max_length=128, null=True, blank=False, default='N/A')
#     spouse_designation = models.CharField(max_length=128, null=True, blank=False, default='N/A')
#     date_of_marriage = models.DateField(null=True, default='', blank=False)
#     marriage_certificate = models.FileField(upload_to='marriage_certificates/', null=True, blank=False)
#     joint_photograph_with_spouse = models.FileField(upload_to='photo_with_spouse/', null=True, blank=False)
#     coursework_grade_sheet = models.FileField(upload_to='grade_sheet/', null=True, blank=False)
#     recommendation_of_guide_for_accomodation = models.FileField(upload_to='guide_recommendation/', null=True, blank=False)
