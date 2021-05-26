
-- Create table principal
create table info_productos_ml
(	fecha_proceso datetime
	id_ml varchar(13),
	seller_id int,
	titulo_producto varchar(150),
	precio_a decimal(10,2),
	moneda_a char(3),
	precio_b decimal(10,2),
	moneda_b char(3),
	fecha_valida_conversion datetime,
	condicion_prod varchar(20),
	garantia varchar(50),
	shipping_free boolean,
	total_vtas_canceladas int,
	total_vtas_completas int,
	total_vtas int,
	url_producto varchar(200)
	);
create index idx_fecha_proceso on  info_productos_ml (fecha_proceso);


-- Crea tabla de logueos para kPI.
create table info_producto_log 
(fecha_inicio datetime,
nombre_api varchar(150),
status_proc varchar(11),
fecha_fin datetime,
duracion decimal(10,2)
);

create index idx_info_log on  info_productos_ml (fecha_inicio);