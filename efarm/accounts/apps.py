from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    icon = 'images/1.png'

    def ready(self):
        import accounts.signals
