from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from real_estate.forms import *
from real_estate.models import *

from profanityfilter import ProfanityFilter
from ukrainian_profanity_filter import ProfanityFilter as UPF


def add_log_reg_forms_to_context(context):
    context['log_form'] = LoginFrom()
    context['reg_form'] = RegistrationForm()


def register_user(request, fail_template, fail_context, success_redirect):
    if request.POST['password'] != request.POST['confirm_password']:
        fail_context['msg'] = 'Password confirmation failed'
        fail_context['log_form'] = LoginFrom()
        return render(request, fail_template, fail_context)
    user = User.objects.create_user(request.POST['username'],
                                    request.POST['email'],
                                    request.POST['password'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()
    login(request, user)
    return redirect(success_redirect)


def login_user(request, fail_template, fail_context, success_redirect):
    user = User.objects.get(username=request.POST['username'])
    if user:
        if user.check_password(request.POST['password']):
            login(request, user)
            return redirect(success_redirect)
        else:
            fail_context['msg'] = 'Wrong password'
            return render(request, fail_template, fail_context)
    fail_context['msg'] = 'User not found'
    return render(request, fail_template, fail_context)


def show_context(request, pk):
    obj = RealEstate.objects.get(id=pk)
    address_src = 'https://maps.google.com/maps?' \
                  'q={country},{state},{city},{address}' \
                  '&t=&z=13&ie=UTF8&iwloc=&output=embed'.format(
        country=obj.country.replace(' ', '%20'),
        state=obj.state.replace(' ', '%20'),
        city=obj.city.replace(' ', '%20'),
        address=obj.address.replace(' ', '%20'),
    )
    context = {'photos': RealEstatePhoto.objects.filter(real_estate_id=pk),
               'obj': obj,
               'address_src': address_src,
               'comments': EstateComment.objects.filter(estate=obj).order_by('-date')}
    add_log_reg_forms_to_context(context)
    return context


class MainPage(View):
    PAGINATOR_COUNT = 4

    def get(self, request, filter_attr=None):
        if filter_attr:
            estate_list = RealEstate.objects.filter(developer__name=filter_attr)
        else:
            estate_list = RealEstate.objects.all()
        estate_paginator = Paginator(estate_list, self.PAGINATOR_COUNT)
        page_num = request.GET.get('page')
        page = estate_paginator.get_page(page_num)
        context = {'pg_count': estate_paginator.count,
                   'page': page}
        add_log_reg_forms_to_context(context)
        context['adv_search'] = AdvancesSearchForm()
        context['active_button'] = 'main'
        return render(request, 'real_estate/main-page.html', context)

    def post(self, request, filter_attr=None):
        log_form = LoginFrom(request.POST)
        reg_form = RegistrationForm(request.POST)
        context = {
            'estate': RealEstate.objects.all(),
            'log_form': log_form,
            'reg_form': reg_form,
            'active_button': 'main',
            'adv_search': AdvancesSearchForm()
        }

        if reg_form.is_valid():
            return register_user(request, 'real_estate/main-page.html', context, '/')
        elif log_form.is_valid() and len(request.POST) == 3:
            return login_user(request, 'real_estate/main-page.html', context, '/')
        elif request.POST.get('search', None):
            query = RealEstate.objects.filter(name__icontains=request.POST['search'])
            # estate_paginator = Paginator(estate_list, self.PAGINATOR_COUNT)
            # page_num = request.GET.get('page')
            # page = estate_paginator.get_page(page_num)
            # context['pg_count'] = estate_paginator.count
            # context['page'] = page
            # return render(request, 'real_estate/main-page.html', context)
        else:
            query = RealEstate.objects.all()
            if request.POST.get('country', None):
                query = query.filter(country=request.POST.get('country', None))
            if request.POST.get('state', None):
                query = query.filter(state=request.POST.get('state', None))
            if request.POST.get('city', None):
                query = query.filter(city=request.POST.get('city', None))
            if request.POST.get('developer', None):
                query = query.filter(developer=request.POST.get('developer', None))
            if request.POST.get('floor', None):
                query = query.filter(floor=request.POST.get('floor', None))
            if request.POST.get('room', None):
                query = query.filter(room=request.POST.get('room', None))
            if request.POST.get('squares', None):
                query = query.filter(squares__gte=request.POST.get('squares', None))
            if request.POST.get('bathrooms', None):
                query = query.filter(bathrooms__gte=request.POST.get('bathrooms', None))
            if request.POST.get('buy_price', None) and int(request.POST.get('buy_price', None)) != 0:
                query = query.filter(buy_price__lte=request.POST.get('buy_price', None))
            if request.POST.get('rent_price', None) and int(request.POST.get('rent_price', None)) != 0:
                query = query.filter(rent_price__lte=request.POST.get('rent_price', None))
            if request.POST.get('build_at', None):
                query = query.filter(build_at__gte=request.POST.get('build_at', None))

        estate_paginator = Paginator(query, self.PAGINATOR_COUNT)
        page_num = request.GET.get('page')
        page = estate_paginator.get_page(page_num)
        context['pg_count'] = estate_paginator.count
        context['page'] = page
        return render(request, 'real_estate/main-page.html', context)


class ShowPage(View):
    def get(self, request, pk):
        context = show_context(request, pk)
        return render(request, 'real_estate/show-page.html', context)

    def post(self, request, pk):
        log_form = LoginFrom(request.POST)
        reg_form = RegistrationForm(request.POST)
        context = show_context(request, pk)
        if reg_form.is_valid():
            return register_user(request, 'real_estate/show-page.html', context, f'/show/{pk}')
        elif log_form.is_valid() and len(request.POST) == 3:
            return login_user(request, 'real_estate/show-page.html', context, f'/show/{pk}')
        else:
            pf = ProfanityFilter()
            upf = UPF()
            comment = upf.censor(pf.censor(request.POST['comment']))
            EstateComment.objects.create(user=request.user,
                                         estate_id=pk,
                                         comment=comment)
            return redirect(f'/show/{pk}')


class PostEstatePage(View):
    def get(self, request):
        context = {'form': EstateForm(), 'active_button': 'add'}
        add_log_reg_forms_to_context(context)
        return render(request, 'real_estate/post-page.html', context)

    def post(self, request):
        log_form = LoginFrom(request.POST)
        reg_form = RegistrationForm(request.POST)
        context = {'form': EstateForm(), 'active_button': 'add'}
        if reg_form.is_valid():
            return register_user(request, 'real_estate/post-page.html', context, f'/add/')
        elif log_form.is_valid() and len(request.POST) == 3:
            return login_user(request, 'real_estate/post-page.html', context, f'/add/')
        else:
            data = request.POST
            obj = RealEstate.objects.create(name=data['name'],
                                            description=data['description'],
                                            country=data['country'],
                                            state=data['state'],
                                            city=data['city'],
                                            address=data['address'],
                                            floor=data['floor'],
                                            rooms=data['rooms'],
                                            bathrooms=data['bathrooms'],
                                            squares=data['squares'],
                                            buy_price=data['buy_price'],
                                            rent_price=data['rent_price'],
                                            developer=BuildCompany.objects.get(id=int(data['developer'])),
                                            main_photo=request.FILES['main_photo'],
                                            build_at=data['build_at'])
            for ph in request.FILES.getlist('photos'):  # important to use .getlist()
                RealEstatePhoto.objects.create(real_estate_id=obj.id,
                                               photo=ph)
            return redirect('/')


class PostDevPage(View):
    context = {'form': DeveloperForm(), 'active_button': 'add-dev'}
    add_log_reg_forms_to_context(context)

    def get(self, request):
        return render(request, 'real_estate/post-page.html', self.context)

    def post(self, request):
        log_form = LoginFrom(request.POST)
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            return register_user(request, 'real_estate/post-page.html', self.context, '/show-dev/')
        elif log_form.is_valid() and len(request.POST) == 3:
            return login_user(request, 'real_estate/post-page.html', self.context, '/show-dev/')
        else:
            BuildCompany.objects.create(name=request.POST['name'],
                                        developer_src=request.POST['developer_src'],
                                        photo=request.FILES['photo'],
                                        )
            return redirect('show-dev/')


class ShowDevPage(View):
    def get(self, request):
        context = {'devs': BuildCompany.objects.all(), 'active_button': 'dev'}
        add_log_reg_forms_to_context(context)
        return render(request, 'real_estate/dev-list-page.html', context)


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class AccountPage(View):
    def get(self, request):
        username = request.user.username if request.user.is_authenticated else None
        msg = None
        user = None
        context = {'user': user, 'msg': msg, 'active_button': 'account'}
        if username:
            user = User.objects.get(username=username)
            context['favourite'] = FavouriteEstate.objects.filter(user=user)
        else:
            context['msg'] = 'Login first'
        return render(request, 'real_estate/account-page.html', context)
