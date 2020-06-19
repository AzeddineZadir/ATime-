from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, DateWidget
from import_export.fields import Field
from .models import Shift, Employe

class ShiftResource(resources.ModelResource):
    employe = fields.Field(
        column_name='id_employé',
        attribute='employe',
        widget=ForeignKeyWidget(Employe, 'pk'))
    number = Field(attribute='number', column_name="numéro")
    nom = Field(attribute='employe__user__first_name', column_name="Nom")
    day = Field(attribute='day', column_name='jours', widget=DateWidget("%d.%m.%Y"))
    prénom = Field(attribute='employe__user__last_name', column_name='Prénom')
    id = Field(attribute='id', column_name="identifiant")
    he = Field(attribute='he', column_name="Heure d'entré")
    hs = Field(attribute='hs', column_name="Heure de sortie")


    class Meta:
        model = Shift
        fields = ('id', 'number', 'day',  'he', 'hs', 'employe', 'nom', 'prénom')
        export_order = ('id', 'number', 'day',  'he', 'hs', 'employe', 'nom', 'prénom')
