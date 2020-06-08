from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import Employe, Shift, Team, Day, Planing
from django.shortcuts import render
from django.http import HttpResponseRedirect


# Register your models here.


class EmployeInline(admin.StackedInline):
    model = Employe
    exclude = ['iwssad', 'finger_id', 'is_uploaded', 'is_delete']


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_name', 'first_name', 'role',)
    actions = ['delete_employe']
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

    # Admin action to delete fingerprint --> Employe
    def delete_employe(self, request, queryset):
        # Check if admin confirm delete and update is_delete to true
        if request.POST.get('valider'):
            for user in queryset:
                user.employe.delete_employe()
            # queryset.update(is_delete=True)
            self.message_user(
                request, "La suppression de {} empreintes a réussi.".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())
        # Return delete confirmation template with queryset to display employe
        return render(request, 'admin/delete_finger.html', context={'objects': queryset, 'opts': User._meta})
    delete_employe.short_description = "Supprimer les empreintes des employes sélectionnés"

    def has_delete_permission(self, request, obj=None):
        return False


class ShiftAdmin(admin.ModelAdmin):

    list_display = ('employe', 'day', 'he1', 'hs1', 'he2', 'hs2')

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


class EmployeAdmin(admin.ModelAdmin):

    list_display = ('id', 'email', 'username',
                    'finger_id', 'is_uploaded', 'is_delete', 'iwssad')

    def id(self, employe):
        return employe.user.id

    def email(self, employe):
        return employe.user.email

    def username(self, employe):
        return employe.user.username

    def has_delete_permission(self, request, obj=None):
        return False


class TeamAdmin(admin.ModelAdmin):
    #actions = ['delete_selected']
    list_display = ['titre', 'manager', 'description']


class DayInline(admin.TabularInline):
    model = Day
    extra = 7
    max_num = 7


class DayAdmin(admin.ModelAdmin):
    list_display = ('jds', 'he1', 'hs1', 'he2', 'hs2')


class PlaningAdmin(admin.ModelAdmin):

    list_display = ('titre', 'description')
    inlines = [DayInline]


admin.site.register(User, UserAdmin)
admin.site.register(Employe, EmployeAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Planing, PlaningAdmin)
admin.site.register(Day, DayAdmin)
