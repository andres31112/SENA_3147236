class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://sofia:12345@localhost:3306/basedatos2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "clave-secreta"
