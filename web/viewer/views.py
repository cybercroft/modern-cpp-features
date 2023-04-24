from django.shortcuts import render
from .utils import Handler 


# -----------------------------------------------------------------------------------------------------------
def home(request):
# -----------------------------------------------------------------------------------------------------------
    """ Introductory view """
    handler = Handler(request)
    if handler.is_empty:
        handler.update()
    return render(request, 'viewer/index.html', handler.get_context())


# -----------------------------------------------------------------------------------------------------------
def version_detail(request, pk):
# -----------------------------------------------------------------------------------------------------------
    """ Specific CPP version view """
    handler = Handler(request)
    return render(request, 'viewer/version/list.html', handler.get_context(version_pk=pk))


# -----------------------------------------------------------------------------------------------------------
def feature_detail(request, pk):
# -----------------------------------------------------------------------------------------------------------
    """ Specific CPP version feature version view """
    handler = Handler(request)
    return render(request, 'viewer/feature/list.html', handler.get_context(feature_pk=pk))