from django.db import models
from django.contrib.auth.models import User

   
class Attendance(models.Model):
    att_id = models.IntegerField(null=False, blank=False,default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance_name = models.CharField(max_length=150)
    # date_created = models.DateField(auto_now_add=True)
    # time_created = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    # marked_attendees = models.ManyToManyField("Attendee")

    def __str__(self):
        return self.attendance_name

    def save(self, *args, **kwargs):
        idcode = Attendance.objects.count() + 1
        self.att_id = idcode
        modified_name = self.attendance_name.replace(" ", "_")
        self.url = f"/attendance/{idcode}/{modified_name[:10]}"

        super().save(*args, **kwargs)


class Attendee(models.Model):
    # attendance = models.ForeignKey('Attendance', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    image = models.TextField() # Will be stored as a base64 string
    status = models.BooleanField(default=False)
    # models.
    attendances = models.ManyToManyField(Attendance)

    def __str__(self):
        return self.name
    
