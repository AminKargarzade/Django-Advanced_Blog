from django.shortcuts import render

# Create your views here.
def indexView(request):
    name = 'Amin'
    context = {'name': name}
    return render(request, 'index.html', context)