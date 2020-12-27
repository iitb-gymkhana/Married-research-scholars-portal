from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import logging
logger = logging.getLogger('__name__')
from django.core.mail import send_mail
from django.db.models import F
from django.conf import settings


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
    spouse_name = models.CharField(max_length=128, null=True, blank=False, default='Name of your Spouse')
    spouse_roll_number = models.CharField(max_length=128, null=True, blank=False, default='N/A')
    spouse_designation = models.CharField(max_length=128, null=True, blank=False, default='N/A')
    marriage_certificate_verified = models.BooleanField(default=False, null=False)
    joint_photograph_with_spouse_verified = models.BooleanField(default=False, null=False)
    coursework_grade_sheet_verified = models.BooleanField(default=False, null=False)
    recommendation_of_guide_for_accomodation_verified = models.BooleanField(default=False, null=False)
    feedback = models.TextField(default='Your Documents are not yet verified!', null=True, blank=True)
    acadsection_feedback = models.TextField(default='', null=True, blank=True, verbose_name="Feedback")
    waitlist_Type1 = models.IntegerField(default=-1, db_index=True, editable=False)
    waitlist_Tulsi = models.IntegerField(default=-1, db_index=True, editable=False)
    waitlist_MRSB = models.IntegerField(default=-1, db_index=True, editable=False)
    date_applied = models.DateTimeField(null=False, default=timezone.now, editable=False, verbose_name="Date Applied")
    verified_time = models.DateTimeField(null=True, blank=True, verbose_name="Date of verification by HCU")
    occupied_Type1 = models.BooleanField(default=False)
    occupied_Tulsi = models.BooleanField(default=False)
    occupied_MRSB = models.BooleanField(default=False)
    # defer_Type1 = models.BooleanField(default=False)
    # defer_Tulsi = models.BooleanField(default=False)
    # defer_MRSB = models.BooleanField(default=False)
    scholarship_awarded_upto = models.DateField(verbose_name="Initially the scholarship awarded up to", null=True, blank=True)
    acad_details_verified = models.BooleanField(default=False, verbose_name="The academic details are verified and found correct")
    acad_details_verification_date = models.DateTimeField(default=timezone.now, verbose_name="Verification Date by Academic Section", null=True)
    application_received_by_hcu_date = models.DateTimeField(verbose_name="Application Received by H.C.Unit Date:", null=True, blank=True)

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"
        # unique_together = ('name', 'roll_number')

    def __str__(self):
        return self.name

    def all_verified(self):
        return bool(self.marriage_certificate_verified and
                    self.coursework_grade_sheet_verified and
                    self.joint_photograph_with_spouse_verified and
                    self.recommendation_of_guide_for_accomodation_verified and
                    self.acad_details_verified
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
                                                        recommendation_of_guide_for_accomodation_verified=True).order_by('verified_time')
                    if not self.occupied_any() and not self.deferred_any():
                        """Either entering into waitlist ot vacating the accomodation"""
                        if flag:
                            """Enter into waitlist"""
                            # qs = Applicant.objects.all().filter(acad_details_verified=True, marriage_certificate_verified=True,
                            #                               joint_photograph_with_spouse_verified=True,
                            #                               coursework_grade_sheet_verified=True,
                            #                               recommendation_of_guide_for_accomodation_verified=True).order_by('date_applied')
                            if self.waitlist_Type1 == -1:
                                self.waitlist_Type1 = 1 + len(qs.filter(waitlist_Type1__gt=0, occupied_Type1=False))
                            if self.waitlist_Tulsi == -1:
                                self.waitlist_Tulsi = 1 + len(qs.filter(waitlist_Tulsi__gt=0, occupied_Tulsi=False))
                            if self.waitlist_MRSB == -1:
                                self.waitlist_MRSB = 1 + len(qs.filter(waitlist_MRSB__gt=0, occupied_MRSB=False))
                        else:
                            """If the applicant has vacated"""
                            if not self.occupied_Tulsi:
                                self.waitlist_Tulsi = 0
                                self.occupied_Type1 = False
                                self.occupied_MRSB = False
                                vacated_list = VacatedList.objects.filter(building='Tulsi')
                                for building in vacated_list:
                                    building.applicant.add(self)
                                    building.save()
                                occupied_list = OccupiedList.objects.filter(building='Tulsi')
                                for building in occupied_list:
                                    building.applicant.exclude(id=self.id)
                                    building.save()
                            elif not self.occupied_Type1:
                                self.waitlist_Type1 = 0
                                self.occupied_Tulsi = False
                                self.occupied_MRSB = False
                                vacated_list = VacatedList.objects.filter(building='Type-1')
                                for building in vacated_list:
                                    building.applicant.add(self)
                                    building.save()
                                occupied_list = OccupiedList.objects.filter(building='Type-1')
                                for building in occupied_list:
                                    building.applicant.exclude(id=self.id)
                                    building.save()
                            elif not self.occupied_MRSB:
                                self.waitlist_MRSB = 0
                                self.occupied_Type1 = False
                                self.occupied_Tulsi = False
                                vacated_list = VacatedList.objects.filter(building='Manas')
                                for building in vacated_list:
                                    building.applicant.add(self)
                                    building.save()
                                occupied_list = OccupiedList.objects.filter(building='Manas')
                                for building in occupied_list:
                                    building.applicant.exclude(id=self.id)
                                    building.save()
                            else:
                                pass
                    # elif self.occupied_any() and not self.deferred_any():
                    #     """If the applicant has occupied any building"""
                    #     if self.occupied_Type1:
                    #         qs_excluded = qs.exclude(id=self.id, waitlist_Type1__lt=0) # exclude the current applicant and all those who are already occupying
                    #         qs_excluded = qs_excluded.exclude(waitlist_Type1__lt=self.waitlist_Type1)
                    #         qs_excluded.update(waitlist_Type1 = F('waitlist_Type1') - 1) # decrease the waitlist number by 1 for all those in the waitlist
                    #         self.waitlist_Type1 = -2
                    #     elif self.occupied_Tulsi:
                    #         qs_excluded = qs.exclude(id=self.id, waitlist_Tulsi__lt=0)  # exclude the current applicant and all those who are already occupying
                    #         qs_excluded = qs_excluded.exclude(waitlist_Tulsi__lt=self.waitlist_Tulsi)
                    #         qs_excluded.update(waitlist_Tulsi=F('waitlist_Tulsi') - 1)  # decrease the waitlist number by 1 for all those in the waitlist
                    #         self.waitlist_Tulsi = -2
                    #     elif self.occupied_MRSB:
                    #         qs_excluded = qs.exclude(id=self.id, waitlist_MRSB__lt=0)  # exclude the current applicant and all those who are already occupying
                    #         qs_excluded = qs_excluded.exclude(waitlist_MRSB__lt=self.waitlist_MRSB)
                    #         qs_excluded.update(waitlist_MRSB=F('waitlist_MRSB') - 1)  # decrease the waitlist number by 1 for all those in the waitlist
                    #         self.waitlist_Tulsi = -2
                    #     else:
                    #         pass
                    #     pass
                    # elif not self.occupied_any() and self.deferred_any():
                    #     if self.defer_Type1:
                    #         self.waitlist_Type1 = -1
                    #     elif self.defer_Tulsi:
                    #         self.waitlist_Tulsi = -1
                    #     elif self.defer_MRSB:
                    #         self.waitlist_MRSB = -1
                    else:
                        pass
                else:
                    """If the all details are not verified by Acad"""
                    self.verified_time = None
                    if not flag:
                        emailid = self.email
                        subject = "Married Research Scholar Portal"
                        message = f"{self.feedback} \n You are requested to modify your application."
                        send_mail(
                            subject=subject,
                            recipient_list=[emailid, ],
                            message=message,
                            from_email=settings.EMAIL_HOST_USER
                        )
                    else:
                        pass
            else:
                if not flag:
                    emailid = self.email
                    subject = "Married Research Scholar Portal"
                    message = f"{self.acadsection_feedback} \n You are requested to modify your application."
                    send_mail(
                        subject=subject,
                        recipient_list=[emailid,],
                        message=message,
                        from_email=settings.EMAIL_HOST_USER
                    )
                else:
                    pass
            
        super(Applicant, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        qs = Applicant.objects.all().filter(acad_details_verified=True, marriage_certificate_verified=True,
                                            joint_photograph_with_spouse_verified=True,
                                            coursework_grade_sheet_verified=True,
                                            recommendation_of_guide_for_accomodation_verified=True).order_by(
            'date_applied')
        qs_excluded = qs.exclude(id=self.id)  # exclude the current applicant and all those who are already occupying
        qs_excluded1 = qs_excluded.exclude(
            waitlist_Type1__lte=self.waitlist_Type1)  # list of students having higher waitlist than current applicant
        qs_excluded1.update(waitlist_Type1=F('waitlist_Type1') - 1)
        qs_excluded2 = qs_excluded.exclude(
            waitlist_Tulsi__lte=self.waitlist_Tulsi)  # list of students having higher waitlist than current applicant
        qs_excluded2.update(waitlist_Tulsi=F('waitlist_Tulsi') - 1)
        qs_excluded3 = qs_excluded.exclude(
            waitlist_MRSB__lte=self.waitlist_MRSB)  # list of students having higher waitlist than current applicant
        qs_excluded3.update(waitlist_MRSB=F('waitlist_MRSB') - 1)

        super(Applicant, self).delete(using=None, keep_parents=False)


class Waitlist(models.Model):
    building = models.CharField(max_length=125, unique=True)
    applicant = models.ManyToManyField(Applicant, blank=True)

    class Meta:
        verbose_name = "Buffered"
        verbose_name_plural = "Buffered"

    def __str__(self):
        return self.building

    def save(self, *args, **kwargs):
        super(Waitlist, self).save(*args, **kwargs)

class OccupiedList(models.Model):
    building = models.CharField(max_length=125, unique=True)
    applicant = models.ManyToManyField(Applicant, blank=True)

    class Meta:
        verbose_name = "Occupied"
        verbose_name_plural = "Occupied"

    def __str__(self):
        return self.building

    def save(self, *args, **kwargs):
        qs = Applicant.objects.all().filter(acad_details_verified=True, marriage_certificate_verified=True,
                                      joint_photograph_with_spouse_verified=True,
                                      coursework_grade_sheet_verified=True,
                                      recommendation_of_guide_for_accomodation_verified=True).order_by('date_applied')
        for student in self.applicant.all():
            if self.building == 'Type-1':
                student.occupied_Type1 = True
                qs_excluded = qs.exclude(id=student.id)  # exclude the current applicant and all those who are already occupying
                qs_excluded = qs_excluded.exclude(waitlist_Type1__lte=student.waitlist_Type1) # list of students having higher waitlist than current applicant
                qs_excluded.update(waitlist_Type1 = F('waitlist_Type1') - 1)
                student.waitlist_Type1 = 0
            elif self.building == 'Tulsi':
                student.occupied_Tulsi = True
                qs_excluded = qs.exclude(
                    id=student.id)  # exclude the current applicant and all those who are already occupying
                qs_excluded = qs_excluded.exclude(
                    waitlist_Tulsi__lte=student.waitlist_Tulsi)  # list of students having higher waitlist than current applicant
                qs_excluded.update(waitlist_Tulsi=F('waitlist_Tulsi') - 1)
                student.waitlist_Tulsi = 0
            elif self.building == 'Manas':
                student.occupied_MRSB = True
                qs_excluded = qs.exclude(
                    id=student.id)  # exclude the current applicant and all those who are already occupying
                qs_excluded = qs_excluded.exclude(
                    waitlist_MRSB__lte=student.waitlist_MRSB)  # list of students having higher waitlist than current applicant
                qs_excluded.update(waitlist_MRSB=F('waitlist_MRSB') - 1)
                student.waitlist_MRSB = 0
            student.save(flag=True)
        super().save(*args, **kwargs)
        # Send an email
        
class VacatedList(models.Model):
    building = models.CharField(max_length=125, unique=True)
    applicant = models.ManyToManyField(Applicant, blank=True)

    class Meta:
        verbose_name = "Vacated"
        verbose_name_plural = "Vacated"

    def __str__(self):
        return self.building
    
    def save(self, *args, **kwargs):
        super(VacatedList, self).save(*args, **kwargs)
        
