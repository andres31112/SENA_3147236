import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevenir la recarga de la página
        setIsLoading(true);
        setMessage('');
        setError('');

        try {
            // Hacemos la petición a la API de Flask
            const response = await fetch('/api/forgot-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email }),
            });

            const data = await response.json();

            if (!response.ok) {
                // Si la respuesta del servidor no es exitosa (ej. 400, 404)
                throw new Error(data.message || 'Algo salió mal.');
            }

            // Mensaje de éxito desde el backend
            setMessage(data.message);

            // Opcional: Redirigir al login después de unos segundos
            setTimeout(() => {
                navigate('/login');
            }, 3000);

        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="form-container">
            <div className="card shadow-lg border-0">
                <div className="card-body p-5">
                    <h2 className="card-title text-center mb-4">Restablecer Contraseña</h2>
                    <p className="text-muted text-center mb-4">
                        Ingresa tu correo y te enviaremos un enlace para recuperar tu cuenta.
                    </p>

                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="email" className="form-label">Correo Electrónico</label>
                            <input
                                type="email"
                                className="form-control form-control-lg"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="tu@email.com"
                                required
                            />
                        </div>

                        {message && <div className="alert alert-success mt-3">{message}</div>}
                        {error && <div className="alert alert-danger mt-3">{error}</div>}

                        <div className="d-grid mt-4">
                            <button type="submit" className="btn btn-primary btn-lg" disabled={isLoading}>
                                {isLoading ? 'Enviando...' : 'Enviar Enlace'}
                            </button>
                        </div>
                    </form>

                    <div className="mt-4 text-center">
                        <Link to="/login" className="text-decoration-none">Volver a Iniciar Sesión</Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ForgotPassword;