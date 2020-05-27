from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import Employe, Shift

# Register your models here.


class EmployeInline(admin.StackedInline):
    model = Employe
    exclude = ['iwssad', 'finger_id', 'is_uploaded', 'is_delete']


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_name', 'first_name', 'role',)
    fieldsets = (
        ('Informations du compte', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('last_name', 'first_name', 'role', 'email'),
        }),
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('username', 'password'),
        }),
        ('Options avancées', {
            'classes': ('collapse', 'wide'),
            'fields': ('groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

    add_fieldsets = (
        ('Informations du compte', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('last_name', 'first_name', 'role', 'email', 'username', 'password1', 'password2'),
        }),

        ('Options avancées', {
            'classes': ('collapse', 'wide'),
            'fields': ('groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

    inlines = [EmployeInline]


class ShiftAdmin(admin.ModelAdmin):

    list_display = ('employe', 'date_heure_e', 'date_heure_s')


class EmployeAdmin(admin.ModelAdmin):

    list_display = ('id', 'email', 'username',
                    'finger_id', 'is_uploaded', 'is_delete', 'team_id')
    actions = ['delete_employe']

    def id(self, employe):
        return employe.user.id

    def email(self, employe):
        return employe.user.email

    def username(self, employe):
        return employe.user.username

    def delete_employe(modeladmin, request, queryset):
        queryset.update(is_delete=True)
    delete_employe.short_description = "Supprimer les empreintes des employes sélectionnés"


admin.site.register(User, UserAdmin)
admin.site.register(Employe, EmployeAdmin)
admin.site.register(Shift, ShiftAdmin)
