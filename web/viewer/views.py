from django.shortcuts import render


# -----------------------------------------------------------------------------------------------------------
def home(request):
# -----------------------------------------------------------------------------------------------------------
    """ Introductory view """
    context = {}
    return render(request, 'viewer/index.html', context)
