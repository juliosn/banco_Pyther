from flask_sqlalchemy import SQLAlchemy

class DatabaseSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if DatabaseSingleton._instance is None:
            DatabaseSingleton._instance = SQLAlchemy()
        return DatabaseSingleton._instance


banco = DatabaseSingleton.get_instance()
