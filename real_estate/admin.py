from django.contrib import admin

from real_estate.models import *


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country', 'city', 'squares', 'floor']


@admin.register(RealEstatePhoto)
class RealEstatePhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'real_estate', 'photo']


@admin.register(BuildCompany)
class BuildCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'developer_src']


@admin.register(EstateComment)
class EstateCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(FavouriteEstate)
class FavouriteEstateAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'estate']
