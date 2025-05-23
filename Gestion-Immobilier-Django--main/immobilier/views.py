from django.shortcuts import render, get_object_or_404, redirect
from .models import Immobilier
from .forms import ImmobilierForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def immobilier_list(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    immobiliers = Immobilier.objects.all()

    if query:
        immobiliers = immobiliers.filter(titre__icontains=query)

    if min_price:
        immobiliers = immobiliers.filter(prix__gte=min_price)

    if max_price:
        immobiliers = immobiliers.filter(prix__lte=max_price)

    paginator = Paginator(immobiliers, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'immobiliers': page_obj,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'immobilier_list.html', context)

@login_required
def immobilier_detail(request, pk):
    immobilier = get_object_or_404(Immobilier, pk=pk)
    return render(request, 'immobilier_detail.html', {'immobilier': immobilier})

@login_required
def immobilier_create(request):
    if request.method == 'POST':
        form = ImmobilierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('immobilier_list')
    else:
        form = ImmobilierForm()
    return render(request, 'immobilier_form.html', {'form': form})

@login_required
def immobilier_update(request, pk):
    immobilier = get_object_or_404(Immobilier, pk=pk)
    if request.method == 'POST':
        form = ImmobilierForm(request.POST, request.FILES, instance=immobilier)
        if form.is_valid():
            form.save()
            return redirect('immobilier_list')
    else:
        form = ImmobilierForm(instance=immobilier)
    return render(request, 'immobilier_form.html', {'form': form})

@login_required
def immobilier_delete(request, pk):
    immobilier = get_object_or_404(Immobilier, pk=pk)
    if request.method == 'POST':
        immobilier.delete()
        return redirect('immobilier_list')
    return render(request, 'immobilier_confirm_delete.html', {'immobilier': immobilier})

def logout_confirm(request):
    return render(request, 'registration/logout-confirm.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, 'compte creer ' + username)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView): 
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout-confirm.html'

# -------- Calendar API and View --------

@csrf_exempt
def immobilier_events_api(request):
   
    events = []
    for immo in Immobilier.objects.all():
        if hasattr(immo, 'date_disponible') and immo.date_disponible:
            events.append({
                "title": immo.titre,
                "start": str(immo.date_disponible),
                "id": immo.id,
            })
    return JsonResponse(events, safe=False)

@login_required
def immobilier_calendar(request):
    return render(request, 'immobilier_calendar.html')