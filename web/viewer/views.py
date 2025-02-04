from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .utils import Handler 
from .models import Feature


# -----------------------------------------------------------------------------------------------------------
def home(request):
# -----------------------------------------------------------------------------------------------------------
    """ Introductory view """
    handler = Handler(request)
    
    if handler.is_empty:
        handler.update()
    
    commons = {}
    feature_map = {}
    feature_qs = Feature.objects.all()
    
    for feature in feature_qs:
        if feature.name in feature_map.keys():
            feature_map[feature.name].append(feature)
        else:
            feature_map[feature.name] = [feature]
    for feature_name, features in feature_map.items():
        if len(features) > 1:
            commons[feature_name] = features
    extras = {
        "common_features": commons,
        "common_features_count": len(commons),
    }
    return render(request, 'viewer/index.html', handler.get_context(extras=extras))


# -----------------------------------------------------------------------------------------------------------
def autocomplete(request):
# -----------------------------------------------------------------------------------------------------------
    """ Autocomplete for search-box """
    handler = Handler(request)
    options = handler.autocomplete()
    return JsonResponse(options, safe=False)


# -----------------------------------------------------------------------------------------------------------
def refresh(request):
# -----------------------------------------------------------------------------------------------------------
    """ Refresh database from files listed """
    handler = Handler(request)
    handler.update()
    return render(request, 'viewer/index.html', handler.get_context())


# -----------------------------------------------------------------------------------------------------------
def version_detail(request, pk):
# -----------------------------------------------------------------------------------------------------------
    """ Specific CPP version view """
    handler = Handler(request)
    return render(request, 'viewer/version/detail.html', handler.get_context(version_pk=pk))


# -----------------------------------------------------------------------------------------------------------
def feature_detail(request, pk):
# -----------------------------------------------------------------------------------------------------------
    """ Specific CPP version feature version view """
    handler = Handler(request)
    return render(request, 'viewer/feature/detail.html', handler.get_context(feature_pk=pk))


# -----------------------------------------------------------------------------------------------------------
def feature_search(request):
# -----------------------------------------------------------------------------------------------------------
    """ Find CPP version feature from search-box """
    name = request.GET.get("search_query", None)
    features = Feature.objects.filter(name=name)
    if features.count() == 0:
        # FIXME: error message?
        return redirect("/")
    elif features.count() == 1:
        feature = features.first()
        return redirect("feature-detail", pk=feature.pk)
    else:
        handler = Handler(request)
        extras = {"features": features}
        return render(request, 'viewer/feature/list.html', handler.get_context(extras=extras))


# -----------------------------------------------------------------------------------------------------------
def feature_find(request):
# -----------------------------------------------------------------------------------------------------------
    """ Find CPP version feature based on tag """
    tag = request.GET.get("tag", None)
    feature = Feature.objects.filter(tag=tag).first()
    if feature:
        url = reverse('feature-detail', args=(feature.pk, ))
        response = {"url": request.build_absolute_uri(url)}
    else:
        response = {"url": None}
    return JsonResponse(response)