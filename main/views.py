from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PerfumeForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from .models import Perfume, Cart, CartItem


def catalog_view(request):
    category = request.GET.get('category')  # ?category=sweet
    if category:
        perfumes = Perfume.objects.filter(category=category)
    else:
        perfumes = Perfume.objects.all()
    return render(request, 'main/catalog.html', {'perfumes': perfumes})


def perfume_detail(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    return render(request, 'main/perfume_detail.html', {'perfume': perfume})


@login_required
def add_perfume(request):
    if request.method == 'POST':
        form = PerfumeForm(request.POST, request.FILES)
        if form.is_valid():
            perfume = form.save(commit=False)
            perfume.user = request.user
            perfume.save()
            return redirect('catalog')  # Переход после добавления
    else:
        form = PerfumeForm()
    return render(request, 'main/add_perfume.html', {'form': form})


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'main/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, perfume_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    perfume = get_object_or_404(Perfume, id=perfume_id)
    item, created = CartItem.objects.get_or_create(cart=cart, perfume=perfume)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')


@login_required
def cart_page(request):
    cart = request.user.cart  # если связываем по OneToOne
    return render(request, 'main/cart.html', {'cart': cart})


def confirm_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.session.get('user_email')
        user = get_user_model().objects.filter(email=email).first()

        if user and user.confirmation_code == code:
            user.is_active = True
            user.confirmation_code = ''
            user.save()
            messages.success(request, 'Аккаунт подтвержден!')
            return redirect('login')
        else:
            messages.error(request, 'Неверный код')

    return render(request, 'main/confirm.html')


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False

            # Генерация кода
            code = str(random.randint(100000, 999999))
            user.confirmation_code = code
            user.save()

            # Отправка письма
            send_mail(
                'Код подтверждения регистрации',
                f'Ваш код: {code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

            request.session['user_email'] = user.email
            return redirect('confirm_code')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Неверные данные')
    return render(request, 'main/login.html')


@login_required
def profile_page(request):
    user = request.user
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        if avatar:
            user.avatar = avatar
            user.save()
            messages.success(request, "Аватар обновлён!")
            return redirect('profile')

    return render(request, 'main/profile_icon.html', {'user': user})


def logout_view(request):
    logout(request)
    return redirect('home')  # замени на нужную тебе страницу


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')
