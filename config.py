import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Chave forte"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(basedir, "data.sqlite")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"

    # Destinatário fixo da turma, exigido pela atividade
    FLASKY_GRUPO = "flaskaulasweb@zohomail.com"

    # E-mail institucional do aluno
    FLASKY_ADMIN = (
        os.environ.get("FLASKY_ADMIN")
        or "guilherme.souto@aluno.ifsp.edu.br"
    )

    FLASKY_NAME = "Guilherme Souto"
    FLASKY_PRONTUARIO = "PT3038483"

    API_KEY = os.environ.get("API_KEY")
    API_URL = os.environ.get("API_URL")
    API_FROM = os.environ.get("API_FROM")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": ProductionConfig,
}
