CREATE TABLE actividades(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
	imagen VARCHAR(255)
);
CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    fechaUltimoAcceso DATE
);
INSERT INTO usuarios (`usuario`, `clave`, `email`, `fechaUltimoAcceso`) VALUES ('root', '$2b$12$MXQZOX/Zr4tXg2w/jTTo8eGi0XVL.GAOz7PCaaXfuQsqb4oYHCvU6', 'root@root.com', '2022-03-01');
INSERT INTO actividades (`id`, `nombre`, `descripcion`, `imagen`) VALUES ('1', 'Levantamiento de peso muerto', 'Ejercicio esencial para fuerza y estabilidad.', '../images/peso_muerto.jpg');
INSERT INTO actividades (`id`, `nombre`, `descripcion`, `imagen`) VALUES ('2', 'Remo para espalda', 'Fortalece la espalda y mejora la resistencia.', '../images/remo_espalda.jpeg');
INSERT INTO actividades (`id`, `nombre`, `descripcion`, `imagen`) VALUES ('3', 'Clase de CrossFit', 'Rutinas intensas para mejorar el acondicionamiento físico.', '../images/crossfit.jpeg')