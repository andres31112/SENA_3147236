const Login = () => {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        // Aquí iría la lógica de autenticación
        console.log('Email:', email);
        console.log('Password:', password);
        alert('Inicio de sesión simulado!');
    };

    return (
        <div className="login-container">
            <h2>Bienvenido</h2>
            <form onSubmit={handleLogin}>
                <div className="input-group">
                    <input
                        type="email"
                        id="email"
                        className="input-field"
                        placeholder=" "
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <label htmlFor="email" className="input-label">Correo Electrónico</label>
                </div>
                <div className="input-group">
                    <input
                        type="password"
                        id="password"
                        className="input-field"
                        placeholder=" "
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <label htmlFor="password" className="input-label">Contraseña</label>
                </div>
                <button type="submit" className="btn-login">
                    <span>Iniciar Sesión</span>
                </button>
            </form>
            <div className="login-options">
                <a href="#">¿Olvidaste tu contraseña?</a>

            </div>
        </div>
    );
};

ReactDOM.render(<Login />, document.getElementById('root'));