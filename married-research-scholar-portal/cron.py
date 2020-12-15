from portal.models import Applicant

def my_scheduled_job():
    print("LoL!")
    pass

def get_waitlist_Tulsi():
    building_name = 'Tulsi'
    # applicants = Applicant.objects.order_by('waitlist_' + building_name)
    print(building_name)