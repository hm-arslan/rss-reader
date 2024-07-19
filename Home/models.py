# Home/models.py

from django.contrib.auth.models import User
from django.db import models


class RssUrls(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    link = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class RssData(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    link = models.TextField(null=True)
    description = models.TextField(null=True)
    budget_start = models.TextField(null=True)
    budget_end = models.TextField(null=True)
    posted_on = models.TextField(null=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.CharField(max_length=50, null=True, blank=True)

    id_rss_url = models.ForeignKey(RssUrls, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class RssSkills(models.Model):
    id = models.AutoField(primary_key=True)
    skills = models.CharField(max_length=255)

    def __str__(self):
        return self.skills

    @classmethod
    def get_or_create_skill(cls, skill_name):
        # Check if the skill already exists
        existing_skill = cls.objects.filter(skills=skill_name).first()
        if existing_skill:
            # Skill already exists, return its ID
            return existing_skill.id
        else:
            # Skill doesn't exist, create a new one and return its ID
            new_skill = cls.objects.create(skills=skill_name)
            return new_skill.id


class SkillsJunction(models.Model):
    junc_id = models.AutoField(primary_key=True)
    rss_data_id = models.ForeignKey(RssData, on_delete=models.CASCADE)
    rss_skills_id = models.ForeignKey(RssSkills, on_delete=models.CASCADE)
