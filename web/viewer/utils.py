from django.conf import settings
from .models import Version, Feature

    
def _reconstruct_database():
    """ Helper function to reconstruct objects if necessary """
    basedir = settings.BASE_DIR
    srcs = list(basedir.parent.glob('CPP*.md'))
    for src in srcs:
        name = src.name.split(".")[0]
        v = Version(name=name, path=src)
        v.save()


class Handler:
    """ Intermediate class to handle requests from views """
    def __init__(self, request=None):
        self.versions = Version.objects.all().order_by("name")
        self.request = request

    @property
    def is_empty(self):
        """ Return version objects found in database """
        return False if self.versions.count() > 0 else True 
    
    def update(self):
        """ Updates db using repo file structure """
        Version.objects.all().delete()
        _reconstruct_database()
        self.versions = Version.objects.all().order_by("name")
        
    def get_context(self, version_pk=None, feature_pk=None):
        """ Get template context """
        context = {
            "title": "modern-cpp-features",
            "cpp_versions": self.versions,
        }
        if version_pk:
            try:
                version = Version.objects.get(pk=version_pk)
                context["cpp_version"] = version
            except Version.DoesNotExist:
                raise ValueError(f"Version (id={version_pk}) does not exist!")
        if feature_pk:
            try:
                feature = Feature.objects.get(pk=feature_pk)
                context["cpp_feature"] = feature 
            except Feature.DoesNotExist:
                raise ValueError(f"Feature (id={feature_pk}) does not exist!")
        return context
        