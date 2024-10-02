-- SELECT vehicle.license_plate FROM vehicle, customer WHERE vehicle.customer_id = customer.id AND customer.user_id = 1;

-- Pieza a buscar
SELECT * FROM repair_part, part WHERE
repair_part.part_id = part.id AND
repair_part.folio = 1;

-- Piezas disponibles al momento de nueva reparación
SELECT * FROM part, repair_part WHERE
part.id != repair_part.part_id AND
part.stock > 0;

SELECT * FROM repair_part;
DESCRIBE repair_part;
SELECT * FROM part;

-- Test de reparación
SELECT * FROM part;
SELECT * FROM repair;
SELECT * FROM repair_part;