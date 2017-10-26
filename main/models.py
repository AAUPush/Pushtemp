from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import math

class Department(models.Model):
   university = models.CharField(max_length=100)
   name = models.CharField(max_length=100)

   def __str__(self):
      return self.name
    
class StudyField(models.Model):
   name = models.CharField(max_length=100)
   code = models.CharField(max_length=5)
   department = models.ForeignKey(Department)
    
   def __str__(self):
      return self.name
        
class Course(models.Model):
   name = models.CharField(max_length=100)
   code = models.CharField(max_length=20)
   studyfield = models.ForeignKey(StudyField)

   def __str__(self):
      return self.name
      
   def get_link_name(self):
        return self.name.replace(' ', '_')

   def get_material_count(self,section):
      materials = self.material_set.filter(section=section)
      return materials.count()


class Section(models.Model):
   year = models.IntegerField()     
   section_number = models.IntegerField()
   studyfield = models.ForeignKey(StudyField)
   course = models.ManyToManyField(Course)
   code = models.CharField(max_length=10)
   
   def __str__(self):
      return self.code
   
class Lecturer(models.Model):
   title_choices = (
      ('Mr.','Mr.'),
      ('Ms.','Ms.'),
      ('Mrs.','Mrs.'),
      ('Dr.','Doctor'),
      ('Prof.','Professor')
   )
   
   title = models.CharField(max_length=15, choices=title_choices)
   user = models.OneToOneField(User)
   name = models.CharField(max_length=100)
   last_name = models.CharField(max_length=100)
   lect_id = models.CharField(max_length=20)
   course = models.ManyToManyField(Course)
   department = models.ForeignKey(Department)
   section = models.ManyToManyField(Section)
   
   def __str__(self):
      return self.title + " " + self.name
      

   #def name(self):
    #  return self.user.first_name + ' ' + self.user.last_name
    
def static_path(instance,filename):
   return 'aaupush/var/www/static/main' + filename
      
class Announcement(models.Model):
   pub_date = models.DateTimeField('Date Published')
   exp_date = models.DateTimeField('Expiry Date')
   message  = models.TextField()
   lecturer = models.ForeignKey(Lecturer)
   section  = models.ManyToManyField(Section)
   file1 = models.FileField(upload_to=static_path, blank=True)
   file2 = models.FileField(upload_to=static_path, blank=True)
   is_urgent = models.BooleanField(default=False)
   count = models.IntegerField()
   
   def __str__(self):
      return 'By: ' + self.lecturer.name
   def get_link_one(self):
      if self.file1:
        return 'main/' + self.file1.url.split('/')[-1]
      else:
        return ""
   def get_link_two(self):
      if self.file2:
        return 'main/' + self.file2.url.split('/')[-1]
      else:
        return ""
   def inc_count(self):
      self.count = self.count + 1
      self.save()
      return True
   
def upload_path(instance, filename):
   return 'aaupush/uploads/' + instance.course.studyfield.department.name + '/' + instance.course.studyfield.name + '/' + instance.course.name + '/' + instance.name + '.' +  instance.ext()

class Material(models.Model):
   name = models.CharField(max_length=100)
   description = models.CharField(max_length=100)
   file = models.FileField(upload_to=upload_path)
   pub_date = models.DateTimeField('Date Published')   
   section = models.ManyToManyField(Section)
   lecturer  = models.ForeignKey(Lecturer)
   course = models.ForeignKey(Course)
   count = models.IntegerField()
   
   class Meta:
      get_latest_by = "pub_date"

   def __str__(self):
      return self.name
   def ext (self):
      return self.file.name.split('.')[-1]
   def file_size(self):
      size_bytes = self.file.size
      i = float(size_bytes/1024)
      return i
   def inc_count(self):
      self.count = self.count + 1
      self.save()
      return True
   
class Quote(models.Model):
   quote = models.CharField(max_length=140)
   author = models.CharField(max_length = 100)
   
   def __str__(self):
      return self.quote   


   
