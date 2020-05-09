from django.apps import AppConfig



class PointageConfig(AppConfig):
    name = 'apps.pointage'

    def ready(self):
        import apps.pointage.signals