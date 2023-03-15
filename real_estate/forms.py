from django import forms

from django.contrib.auth.models import User

from .widgets import RangeInput

from real_estate.models import RealEstate, BuildCompany


class EstateForm(forms.ModelForm):
    country = forms.ChoiceField(widget=forms.Select(attrs={'class': 'countries', 'name': 'country', 'id': 'countryId'}))
    state = forms.ChoiceField(widget=forms.Select(attrs={'class': 'states', 'name': 'state', 'id': 'stateId'}))
    city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'cities', 'name': 'city', 'id': 'cityId'}))
    photos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = RealEstate
        fields = ['country', 'state', 'city', 'address', 'developer', 'floor', 'rooms', 'squares', 'bathrooms', 'name',
                  'description', 'buy_price', 'rent_price', 'build_at', 'main_photo', 'photos']


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = BuildCompany
        fields = '__all__'


class LoginFrom(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']


class AdvancesSearchForm(forms.ModelForm):
    country = forms.ChoiceField(widget=forms.Select(attrs={'class': 'countries', 'name': 'country', 'id': 'countryId'}))
    state = forms.ChoiceField(widget=forms.Select(attrs={'class': 'states', 'name': 'state', 'id': 'stateId'}))
    city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'cities', 'name': 'city', 'id': 'cityId'}))

    class Meta:
        model = RealEstate
        fields = ['country', 'state', 'city', 'developer', 'floor', 'rooms', 'squares', 'bathrooms',
                  'buy_price', 'rent_price', 'build_at']

    def __init__(self, *args, **kwargs):
        super(AdvancesSearchForm, self).__init__(*args, **kwargs)
        self.fields['country'].required = False
        self.fields['state'].required = False
        self.fields['city'].required = False
        self.fields['developer'].required = False
        self.fields['floor'].required = False
        self.fields['rooms'].required = False
        self.fields['squares'].required = False
        self.fields['bathrooms'].required = False
        self.fields['buy_price'].required = False
        self.fields['rent_price'].required = False
        self.fields['build_at'].required = False
