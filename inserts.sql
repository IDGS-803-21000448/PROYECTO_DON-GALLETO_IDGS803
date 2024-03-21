use proyecto_don_galleto;

INSERT INTO materias_primas (nombre, fecha_caducidad, cantidad_disponible, create_date)
VALUES ('Harina', '2024-05-01', 100.0, NOW()),
       ('Azúcar', '2024-06-01', 50.0, NOW());


INSERT INTO recetas (nombre, descripcion, num_galletas, create_date)
VALUES ('Galletas de Chocolate', 'Galletas con trozos de chocolate', 24, NOW()),
       ('Galletas de Vainilla', 'Galletas sabor vainilla', 30, NOW());


INSERT INTO receta_detalle (receta_id, materia_prima_id, cantidad_necesaria, merma_porcentaje)
VALUES (1, 1, 2.5, 0.05),
       (1, 2, 1.0, 0.02);


INSERT INTO mermas (materia_prima_id, tipo, cantidad, descripcion, fecha)
VALUES (1, 'Daño', 5, 'Paquete roto', NOW());

INSERT INTO alertas (nombre, descripcion, fechaAlerta, estatus) VALUES ('Alerta 1', 'Descripción de la alerta 1', '2024-03-18 10:00:00', 1);
INSERT INTO alertas (nombre, descripcion, fechaAlerta, estatus) VALUES ('Alerta 2', 'Descripción de la alerta 2', '2024-03-19 12:00:00', 0);
INSERT INTO alertas (nombre, descripcion, fechaAlerta, estatus) VALUES ('Alerta 3', 'Descripción de la alerta 3', '2024-03-20 15:00:00', 1);
INSERT INTO alertas (nombre, descripcion, fechaAlerta, estatus) VALUES ('Alerta 4', 'Descripción de la alerta 4', '2024-03-21 17:00:00', 0);