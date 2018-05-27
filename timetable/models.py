from django.db import models


class Class(models.Model):
    class Meta:
        db_table = "Class"

    number = models.IntegerField()
    liter = models.CharField(max_length=1)
    teacher_id = models.IntegerField(default=0)


class Teacher(models.Model):
    class Meta:
        db_table = "Teacher"

    name = models.CharField(max_length=15)
    sur_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class Subject(models.Model):
    class Meta:
        db_table = "Subject"

    name = models.CharField(max_length=30)
    difficulty = models.IntegerField()
    need_spec_audience = models.BooleanField(default=False)


class Audience(models.Model):
    class Meta:
        db_table = "Audience"

    number = models.IntegerField()
    special = models.IntegerField(default=0)
    name = models.CharField(null=True, max_length=30)


class Workload(models.Model):
    class Meta:
        db_table = "Workload"

    teacher_id = models.IntegerField()
    class_number = models.IntegerField()
    class_liter = models.CharField(max_length=1)
    subject_id = models.IntegerField()


class StudyPlan(models.Model):
    class Meta:
        db_table = "StudyPlan"

    subject_id = models.IntegerField()
    class_number = models.IntegerField()
    hours = models.IntegerField()


class Scheduele(models.Model):
    class Meta:
        db_table = "Scheduele"

    class_number = models.IntegerField()
    class_liter = models.CharField(max_length=1)
    weekday = models.IntegerField()
    lesson_number = models.IntegerField()
    subject_id = models.IntegerField()
    audience_id = models.IntegerField(null=True)
    teacher_id = models.IntegerField()