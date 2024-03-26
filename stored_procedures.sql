
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
DROP procedure IF EXISTS modificar_usuario;
DELIMITER //
CREATE PROCEDURE modificar_usuario(
    IN p_id INT,
    IN p_nombre VARCHAR(50),
    IN p_puesto VARCHAR(50),
    IN p_rol VARCHAR(50),
    IN p_estatus VARCHAR(50),
    IN p_usuario VARCHAR(50),
    IN p_contrasena VARCHAR(50)
)
BEGIN
    UPDATE user
    SET
        nombre = p_nombre,
        puesto = p_puesto,
        rol = p_rol,
        estatus = p_estatus,
        usuario = p_usuario,
        contrasena = p_contrasena
    WHERE id = p_id;
END//
DELIMITER ;


#------------PROVEEDORES----------------
DROP PROCEDURE IF EXISTS agregar_proveedor;
DELIMITER //
CREATE PROCEDURE agregar_proveedor (
    IN p_nombre VARCHAR(100),
    IN p_direccion VARCHAR(255),
    IN p_telefono VARCHAR(15),
    IN p_nombre_vendedor VARCHAR(100),
    IN p_estatus INT
)
BEGIN
    INSERT INTO proveedores (nombre, direccion, telefono, nombre_vendedor, estatus)
    VALUES (p_nombre, p_direccion, p_telefono, p_nombre_vendedor, p_estatus);
END //
DELIMITER ;