import markdown as md
from django.utils.safestring import mark_safe
from django.db import models

    
# -----------------------------------------------------------------------------------------------------------
def md_to_html(md_text):
# -----------------------------------------------------------------------------------------------------------
    md_extensions = [
        'toc',
        'nl2br',
        'tables',
        'fenced_code',
        'codehilite',
    ]
    md_configs = {
        "codehilite": {
            'guess_lang': False,
            'use_pygments': True,
            'noclasses': True,
            'force_language': 'cpp',
            'pygments_style': 'default',
        },
    }
    parser = md.Markdown(extensions=md_extensions, extension_configs=md_configs)
    md_text = md_text.replace("```c++", "```cpp")
    return mark_safe(parser.convert(md_text))


# -----------------------------------------------------------------------------------------------------------
class Version(models.Model):
# -----------------------------------------------------------------------------------------------------------
    """ Object to group all CPP version language/library features """
    name = models.CharField("Name", max_length=150)
    path = models.CharField("Path", max_length=255)
    overview = models.TextField("Overview", blank=True)

    def __str__(self):
        return self.name 

    @property
    def has_overview(self):
        return True if len(self.overview) else False
        
    @property
    def to_html(self):
        with open(self.path, 'r') as f:
            md_text= f.read()
        return md_to_html(md_text)
    
        
# -----------------------------------------------------------------------------------------------------------
class Section(models.Model):
# -----------------------------------------------------------------------------------------------------------
    """ Object to illustrate a CPP version section """
    version = models.ForeignKey(Version, on_delete=models.CASCADE)        
    title = models.CharField("Title", max_length=150, default="")   
    description = models.TextField("Description", blank=True)
    
    @property
    def description_html(self):
        return md_to_html(self.description)
   
    
# -----------------------------------------------------------------------------------------------------------
class Feature(models.Model):
# -----------------------------------------------------------------------------------------------------------
    """ Object to describe a CPP version language/library feature """
    class Types(models.TextChoices):
        LANGUAGE  = "LANGUAGE",  "Language Feature"
        LIBRARY = "LIBRARY", "Library Feature"

    version = models.ForeignKey(Version, on_delete=models.CASCADE)        
    type = models.CharField("Type", max_length=30, choices=Types.choices, default=Types.LANGUAGE)
    title = models.CharField("Title", max_length=150, default="")   
    name = models.CharField("Name", max_length=150, default="")   
    tag = models.CharField("Tag", max_length=100, default="")   
    description = models.TextField("Description", blank=True)
    
    def __str__(self):
        return self.name 
   
    @staticmethod
    def as_keyword(name):
        return name.replace("\\", "").replace("`", "").replace(" ", "-")
    
    @property
    def type_label(self):
        return f"{self.get_type_display()}"

    @property
    def description_html(self):
        return md_to_html(self.description)