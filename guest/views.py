from django.shortcuts import render

# Create your views here.

def home(request):
    just_logged_out = request.session.pop('just_logged_out', False)
    context = {
        'just_logged_out': just_logged_out
    }
    return render(request, 'guest/home.html', context)

