
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Immobilier
from .forms import ImmobilierForm
from .models import Reservation 
from .models import Reservation, Notification
from django.contrib.auth.models import User
from django.http import HttpResponse


@login_required
def immobilier_list(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    immobiliers = Immobilier.objects.filter(disponible=True)

    if query:
        immobiliers = immobiliers.filter(titre__icontains=query)
    if min_price:
        immobiliers = immobiliers.filter(prix__gte=min_price)
    if max_price:
        immobiliers = immobiliers.filter(prix__lte=max_price)

    paginator = Paginator(immobiliers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'immobilier_list.html', {
        'immobiliers': page_obj,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    })

@login_required
def immobilier_detail(request, pk):
    immobilier = get_object_or_404(Immobilier, pk=pk)
    reservation = None
    
    if request.user.is_authenticated:
        reservation = Reservation.objects.filter(
            user=request.user, 
            immobilier=immobilier
        ).first()

    return render(request, 'immobilier_detail.html', {
        'immobilier': immobilier,
        'reservation': reservation,
        'is_reserved': reservation is not None
    })  


@login_required
def immobilier_detail(request, pk):
    immobilier = get_object_or_404(Immobilier, pk=pk)
    return render(request, 'immobilier_detail.html', {'immobilier': immobilier})

@login_required
def immobilier_create(request):
    if not request.user.is_staff:
        return redirect('immobilier_list')
    
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
    if not request.user.is_staff:
        return redirect('immobilier_list')
    
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
    if not request.user.is_staff:
        return redirect('immobilier_list')
    
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
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}')
            login(request, user)
            return redirect('immobilier_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout-confirm.html'



@login_required
def reserve_apartment(request, pk):
    immobilier = get_object_or_404(Immobilier, pk=pk)
    if request.method == 'POST':
        if Reservation.objects.filter(user=request.user, immobilier=immobilier).exists():
            messages.warning(request, "Vous avez déjà réservé cet appartement!")
        else:
            reservation = Reservation.objects.create(user=request.user, immobilier=immobilier)
           
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                Notification.objects.create(
                    user=admin,
                    message=f"Nouvelle réservation par {request.user.username} pour {immobilier.titre}"
                )
            messages.success(request, "Réservation effectuée avec succès!")
    return redirect('immobilier_detail', pk=pk)
def rabat_map(request):
        return render(request, 'rabat_map.html')



