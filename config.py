import os

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:3112@127.0.0.1:3306/institucion_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta para la seguridad de la aplicación
    # Usa una variable de entorno para producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-llave-secreta-para-proteger-las-sesiones'

    # -------------------------------------------------------------
    # Configuración de Flask-Mail para el envío de correos
    # -------------------------------------------------------------
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'jsuarezhe04@gmail.com'
    MAIL_PASSWORD = 'qutjgxhnangevraz'
    MAIL_DEFAULT_SENDER = 'jsuarezhe04@gmail.com'