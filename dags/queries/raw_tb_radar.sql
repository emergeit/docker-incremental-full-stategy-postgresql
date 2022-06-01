insert into postgres.target.tb_radar
	select 
		id,
		uuid,
		radar_id,
		license_plate,
		vehicle_make,
		vehicle_model,
		vehicle_color,
		velocity,
		velocity_limit,
		country_code,
		state_name,
		created_at,
		updated_at,
		sourceTime
	FROM postgres.source.tb_radar
	where updated_at > '${DATE}'
ON CONFLICT ON CONSTRAINT tb_radar_pk DO UPDATE
	SET
		id = excluded.id,
		uuid = excluded.uuid,
		radar_id = excluded.radar_id,
		license_plate = excluded.license_plate,
		vehicle_make = excluded.vehicle_make,
		vehicle_model = excluded.vehicle_model,
		vehicle_color = excluded.vehicle_color,
		velocity = excluded.velocity,
		velocity_limit = excluded.velocity_limit,
		country_code = excluded.country_code,
		state_name = excluded.state_name,
		created_at = excluded.created_at,
		updated_at = excluded.updated_at,
		sourceTime = excluded.sourceTime
	RETURNING *;