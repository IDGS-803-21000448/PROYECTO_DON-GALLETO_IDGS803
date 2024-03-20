
-- Crear store procedure para agregar usuarios
DELIMITER //
CREATE PROCEDURE agregar_usuario(
    IN nombre VARCHAR(80),
    IN puesto VARCHAR(80),
    IN rol VARCHAR(80),
    IN estatus VARCHAR(80),
    IN usuario VARCHAR(80),
    IN contrasena VARCHAR(80)
)
BEGIN
    INSERT INTO user (nombre, puesto, rol, estatus, usuario, contrasena)
    VALUES (nombre, puesto, rol, estatus, usuario, contrasena);
END //
DELIMITER ;



-- Crear store procedure para modificar usuarios
DELIMITER //
CREATE PROCEDURE modificar_usuario(
    IN id_user INT,
    IN nombre VARCHAR(80),
    IN puesto VARCHAR(80),
    IN rol VARCHAR(80),
    IN estatus VARCHAR(80),
    IN usuario VARCHAR(80),
    IN contrasena VARCHAR(80)
)
BEGIN
    UPDATE user SET
        nombre = nombre,
        puesto = puesto,
        rol = rol,
        estatus = estatus,
        usuario = usuario,
        contrasena = contrasena
    WHERE id_user = id_user;
END //
DELIMITER ;

