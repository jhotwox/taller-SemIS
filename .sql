-- SELECT vehicle.license_plate FROM vehicle, customer WHERE vehicle.customer_id = customer.id AND customer.user_id = 1;

-- Pieza a buscar
SELECT * FROM repair_part, part WHERE
repair_part.part_id = part.id AND
repair_part.folio = 1;

-- Piezas disponibles al momento de nueva reparación
SELECT * FROM part, repair_part WHERE
part.id != repair_part.part_id AND
part.stock > 0;

-- Licencia de vehículo registrada en repair
SELECT folio FROM repair WHERE
license_plate = 'BBB111';

-- Test de reparación
SELECT * FROM part;
SELECT * FROM repair;
SELECT * FROM repair_part;

SELECT COUNT(*) FROM repair_part WHERE folio = 2 AND part_id = 2;