
import os

db_host = os.environ.get('DB_HOST', default='localhost')
db_name = os.environ.get('DB_NAME', default='hms')
db_user = os.environ.get('DB_USERNAME', default='hms')
db_password = os.environ.get('DB_PASSWORD', default='')
db_port = os.environ.get('DB_PORT', default='5432')

SQLALCHEMY_TRACK_MODIFICATIONS = False

env = os.environ.get("FLASK_ENV", "development")
if env == "production":
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
else:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"




# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/hms_db'

# class Config:
#     SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
#
#
# class DevelopmentConfig(Config):
#     SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
#
#
# class ProductionConfig(Config):
#     uri = os.environ.get("DATABASE_URL")
#     if uri and uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql://", 1)
#     SQLALCHEMY_DATABASE_URI = uri
#
#
# env = os.environ.get("FLASK_ENV", "development")
# print(env)
# if env == "production":
#     config_string = ProductionConfig
# else:
#     config_string = DevelopmentConfig
