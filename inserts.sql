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
