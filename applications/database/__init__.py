from applications.model import init_model


class DatabaseService:
    instance = None

    def __init__(self):
        pass

    def init_app(self, instance):
        self.instance = instance
        init_model(instance)


database_service = DatabaseService()
