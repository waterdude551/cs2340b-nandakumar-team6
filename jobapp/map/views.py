from django.shortcuts import render

# Create your views here.
def show(request):
    print("hiii")
    return render(request, "map/map.html")