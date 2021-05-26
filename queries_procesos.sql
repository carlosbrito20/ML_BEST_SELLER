-- Tiempo de ejecución de las API y el proceso completo (Total de registros).
select 
nombre_api as proceso_name, 
date(fecha_inicio) as fecha, 
round(sum(Round((time_to_sec(fecha_fin)-time_to_sec(fecha_inicio)),2))/60,2) as time_minut
from productos_ml.info_producto_log 
group by nombre_api, date(fecha_inicio);

-- Cantidad de registro por día
select 
fecha_proceso, 
count(1) as cantidad 
from productos_ml.info_productos_ml
group by fecha_proceso
order by fecha_proceso desc;

-- Tiempo total de insert en tabla principal
select 
nombre_api as proceso_name, 
date(fecha_inicio) as fecha, 
round(sum(Round((time_to_sec(fecha_fin)-time_to_sec(fecha_inicio)),2))/60,2) as time_minut
from productos_ml.info_producto_log where nombre_api ='Carga tabla principal'
group by nombre_api, date(fecha_inicio);

-- Se Busca cantidad de productos nuevos --> No hay para MLB
select condicion_prod_1, condicion_prod_2
 from productos_ml.info_productos_ml
 group by condicion_prod_1, condicion_prod_2;