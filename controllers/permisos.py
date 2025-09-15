# permisos.py
# Roles y permisos directamente en el backend
ROLE_PERMISSIONS = {
    'Super Admin': [
        'gestion_usuarios', 'gestion_asignaturas', 'registro_calificaciones',
        'gestion_comunicados', 'gestion_inventario', 'gestion_matriculas',
        'gestion_electoral', 'crear_roles', 'ver_roles', 'editar_roles', 'eliminar_roles'
    ],
    'Profesor': [
        'ver_calificaciones_propias', 'ver_horario_clases', 'ver_lista_estudiantes',
        'registrar_calificaciones', 'gestion_comunicados_profesor'
    ],
    'Estudiante': [
        'ver_calificaciones', 'ver_horario', 'ver_historial_academico',
        'inscripcion_materias', 'ver_comunicaciones_estudiante', 'ver_estado_cuenta',
        'editar_perfil', 'acceso_soporte'
    ],
    'Padre': [
        'ver_calificaciones_hijo', 'ver_horario_hijo', 'ver_comunicaciones_padre',
        'acceso_soporte'
    ]
}
