import markdown_deux as md
from django.utils.safestring import mark_safe
from django.db import models


class Version(models.Model):
    """ Object to group all CPP version language/library features """
    name = models.CharField("Name", max_length=150)
    path = models.CharField("Path", max_length=255)

    def __str__(self):
        return self.name 

    def to_html(self):
        with open(self.path, 'r') as f:
            temp_md= f.read()
        return mark_safe(md.markdown(temp_md))
    
    
class Feature(models.Model):
    """ Object to describe a CPP version language/library feature """
    class Types(models.TextChoices):
        LANGUAGE  = "LANGUAGE",  "Language Feature"
        LIBRARY = "LIBRARY", "Library Feature"

    version = models.ForeignKey(Version, on_delete=models.CASCADE)        
    type = models.CharField("Type", max_length=30, choices=Types.choices, default=Types.LANGUAGE)
    name = models.CharField("Name", max_length=150)   
    description = models.TextField("Description", blank=True)
    
    def __str__(self):
        return self.name 
    
    @property
    def type_label(self):
        return f"{self.get_type_display()}"
