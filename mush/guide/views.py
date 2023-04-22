from django.shortcuts import render


def guide(request):
    ctx = {}

    return render(request, 'guide/guide.html', ctx)
