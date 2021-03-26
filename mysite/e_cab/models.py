from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

class Cabinet_vote(models.Model):

    cabinet_vote = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.cabinet_vote

class Chair_vote(models.Model):

    chair_vote = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.chair_vote


class Motion(models.Model):
    Final_Vote_Choices = [
        ('Motion Approved', 'Motion Approved'),
        ('Motion Vetoed', 'Motion Vetoed'),
        ('Motion Tabled', 'Tabled Until the next Session'),
    ]
    id              = models.AutoField(primary_key=True)
    title           = models.CharField(max_length=100)
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    ministry        = models.CharField(max_length=100)
    pdf             = models.FileField(upload_to='legs/pdfs/')
    cabinet_vote    = models.ForeignKey(Cabinet_vote, on_delete=models.CASCADE, blank=True, null=True)
    chair_vote      = models.ForeignKey(Chair_vote, on_delete=models.CASCADE, blank=True, null=True)
    summary         = models.CharField(max_length=250, blank=True, default="No Summary")
    Votes_Favor     = models.IntegerField(default=0, null=True)
    Votes_Against   = models.IntegerField(default=0, null=True)
    Votes_Nodesc    = models.IntegerField(default=0, null=True)
    final_vote      = models.CharField(
        max_length=20,
        choices=Final_Vote_Choices,
        default= 'Motion Tabled'
         )


    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)


    @property
    def total_votes(self):
        return self.Votes_Favor + self.Votes_Against

    #Simple majority - 50℅ + 1 of members present and voting
    @property
    def simple_majority(self):
        val = self.total_votes * .50
        new_val = round(val, ) + 1
        return (new_val)

    @property
    def pass_crit(self):
        if self.Votes_Favor >= self.simple_majority:
            return True
        else:
            return False













