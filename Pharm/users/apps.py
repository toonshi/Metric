from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def  ready(self):
        import users.signals    # noqa
        # Import all the models in this app at startup to register them with the admin site automatically
        # (if Django is running with the "--create-admin" option). This makes it easy for developers to add
        # new models without having to manually register each model in admin.py. If you want more control over
        # new models without having to manually specify them in admin.py or modify the admin site settings.
        # https://docs.djangoproject.com/en/3.2/ref/applications/#django.apps.AppConfig.ready
       # import users.models  # noqa: F401
