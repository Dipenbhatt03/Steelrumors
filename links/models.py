from __future__ import unicode_literals
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models import  Count

class LinkVoteCountManager(models.Manager):
    def get_queryset(self):
        return super(LinkVoteCountManager, self).get_queryset().annotate(
            votes=Count('vote')).order_by('-rank_scores','votes')


class Link(models.Model):
    title=models.CharField("HeadLine",max_length=200)
    submitter=models.ForeignKey(User)
    submitted_on=models.DateTimeField(auto_now_add=True)
    rank_scores=models.FloatField(default=0.0)
    url=models.URLField("URL",max_length=226,blank=True)
    description=models.TextField(blank=True)
    with_votes=LinkVoteCountManager()
    object=models.Manager()
    #class Meta:
     #   verbose_name_plural="Links"
    def get_absolute_url(self):
        return reverse('link_detail',kwargs={"pk":self.id})
    def __unicode__(self):
        return self.title

    def Set_Scores(self):
        GRAVITY = 1.8
        SEC_IN_HOUR = float(5)
        delta = now() - self.submitted_on
        item_hour = delta.total_seconds() / SEC_IN_HOUR
        votes = self.votes-1;
        self.rank_scores=votes/pow((item_hour+2),GRAVITY)
        self.save()


class Vote(models.Model):
    voter=models.ForeignKey(User)
    link=models.ForeignKey(Link)
   # class Meta:
    #    verbose_name_plural="Votes"
    def __unicode__(self):
        return "%s voted %s" %(self.voter.username,self.link.title)

class UserProfile(models.Model):
    user=models.OneToOneField(User,unique=True)
    bio=models.TextField(null=True)
    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender,instance,created,**kwargs):
    if created:
        profile,created=UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile,sender=User)
