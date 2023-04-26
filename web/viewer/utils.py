import re
from django.db.models import Q
from django.conf import settings
from .models import Version, Feature, Section


# -----------------------------------------------------------------------------------------------------------
def _construct_version_data(version):
# -----------------------------------------------------------------------------------------------------------
    with open(version.path, 'r') as f:
        text = f.read()
        text = text .replace("```c++", "```cpp")
        pattern = r"- \[(.+)\]\((.+)\)"
        sections = text.split("\n## ")
        features = {}
        num_created = 0
        num_complete = 0
        for section in sections:
            if section.startswith("Overview"):
                lines = section.split("\n")
                feature_type = Feature.Types.LANGUAGE
                overview = []
                for line in lines:
                    if line.startswith("- "):
                        match = re.search(pattern, line)
                        name = match.group(1)
                        tag = match.group(2)
                        name = name.replace("\\", "")
                        tag = tag.lstrip("#")
                        feature = Feature(version=version, name=name, tag=tag, type=feature_type) 
                        feature.save()
                        features[Feature.as_keyword(name)] = feature
                        num_created += 1
                    elif line.startswith("C++"):
                        if "library" in line:
                            feature_type = Feature.Types.LIBRARY
                        elif "language" in line:
                            feature_type = Feature.Types.LANGUAGE
                    else:
                        info = line.strip()
                        if len(info):
                            overview.append(info)
                if len(overview):
                    version.overview = "\n".join(overview[1:])
                    version.save()
            else:
                if "### " in section:
                    subsections = section.split("\n### ")
                    for subsection in subsections:
                        lines = subsection.split("\n")
                        if len(lines):
                            name = lines[0].lower()
                            if not name.startswith("c++"):
                                keyword = Feature.as_keyword(name)
                                feature = features.get(keyword, None)
                                if feature:
                                    feature.title = lines[0]                    
                                    feature.description = "\n".join(lines[1:])
                                    feature.save()
                                    num_complete += 1
                                else:
                                    print(f"Warning: [{version.name}] feature keyword: '{keyword}' not found!")
                else:
                    lines = section.split("\n")
                    if len(lines):
                        title = lines[0]
                        if not title.startswith("#"):
                            s = Section(version=version)
                            s.title = title                    
                            s.description = "\n".join(lines[1:])
                            s.save()
        assert(num_complete == num_created)

    
# -----------------------------------------------------------------------------------------------------------
def _construct_version(path):
# -----------------------------------------------------------------------------------------------------------
    name = path.name.split(".")[0]
    name = name.replace("CPP", "C++")
    version = Version(name=name, path=path)
    version.save()
    return version
    
    
# -----------------------------------------------------------------------------------------------------------
def _reconstruct_database():
# -----------------------------------------------------------------------------------------------------------
    """ Helper function to reconstruct objects if necessary """
    basedir = settings.BASE_DIR
    srcs = list(basedir.parent.glob('CPP*.md'))
    for src in srcs:
        version = _construct_version(src)
        _construct_version_data(version)


# -----------------------------------------------------------------------------------------------------------
class Handler:
# -----------------------------------------------------------------------------------------------------------
    """ Intermediate class to handle requests from views """
    def __init__(self, request=None):
        self.versions = Version.objects.all().order_by("name")
        self.request = request

    @property
    def is_empty(self):
        """ Return version objects found in database """
        return False if self.versions.count() > 0 else True 

    def search(self, data='term'):
        q = self.request.GET.get(data, None)
        return Feature.objects.filter(name__icontains=q, title__icontains=q)
    
    def autocomplete(self, data='term'):
        features = self.search(data)
        options = [feature.name for feature in features]
        return options
    
    def update(self):
        """ Updates db using repo file structure """
        Version.objects.all().delete()
        _reconstruct_database()
        self.versions = Version.objects.all().order_by("name")
        
    def get_context(self, version_pk=None, feature_pk=None, extras=None):
        """ Get template context """
        context = {
            "title": "modern-cpp-features",
            "cpp_versions": self.versions,
            "extras": extras,
        }
        if version_pk:
            try:
                version = Version.objects.get(pk=version_pk)
                features = Feature.objects.filter(version=version)
                context["cpp_version"] = version
                context["cpp_sections"] = Section.objects.filter(version=version)
                context["cpp_features_lang"] = features.filter(type=Feature.Types.LANGUAGE)
                context["cpp_features_lib"] = features.filter(type=Feature.Types.LIBRARY)
            except Version.DoesNotExist:
                raise ValueError(f"Version (id={version_pk}) does not exist!")
        if feature_pk:
            try:
                feature = Feature.objects.get(pk=feature_pk)
                context["cpp_feature"] = feature 
            except Feature.DoesNotExist:
                raise ValueError(f"Feature (id={feature_pk}) does not exist!")
        return context
        

# -----------------------------------------------------------------------------------------------------------
def setup():
# -----------------------------------------------------------------------------------------------------------
    versions = Version.objects.all()
    if versions.count() == 0:
        _reconstruct_database()
