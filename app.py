# app.py
from flask import Flask
from flask_login import LoginManager
from config import Config
from extensions import db   


# Inicialización de la base de datos

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from controllers.models import Usuario
        return Usuario.query.get(int(user_id))

    # Importar blueprints después de inicializar la app
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.estudiantes import estudiantes_bp
    from routes.profesor import profesor_bp
    from routes.padres import padre_bp

    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(estudiantes_bp)
    app.register_blueprint(profesor_bp)
    app.register_blueprint(padre_bp)

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app

def create_initial_data(app):
    from controllers.models import Usuario, Administrador
    with app.app_context():
        if not Usuario.query.filter_by(noIdentidad='000000000').first():
            super_admin = Usuario(
                tipoDoc='cc',
                noIdentidad='000000000',
                nombre='Super',
                apellido='Administrador',
                correo='admin@institucion.edu',
                estado='activo',
                rol='administrador'
            )
            super_admin.set_password('admin123')
            db.session.add(super_admin)
            db.session.commit()
            admin = Administrador(usuarioId=super_admin.id)
            db.session.add(admin)
            db.session.commit()
            print("Usuario 'Super Administrador' creado con contraseña 'admin123'.")

if __name__ == '__main__':
    app = create_app()
    create_initial_data(app)
    app.run(debug=True)