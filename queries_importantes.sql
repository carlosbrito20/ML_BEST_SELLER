-- Indica cantidad de publicaciones por seller 
select 
seller_id, 
count(1) as cant_publicaciones 
from productos_ml.info_productos_ml  where  fecha_proceso = current_date()
group by seller_id
order by 2 desc;

--- Promedio del precio por seller en modena BRL y USD
select 
 seller_id, 
 moneda_a as moneda_BRL, 
 (sum(precio_a)/count(1)) as precio_brl_promedio, 
 moneda_b as moneda_usd, 
 (sum(precio_b)/ count(1)) as precio_usd_promedio 
 from productos_ml.info_productos_ml  where  fecha_proceso = current_date()
group by seller_id, moneda_a, moneda_b
order by 5 desc;

-- Precio promedio en dolares
select 
 moneda_b as moneda_usd, 
 count(1) as cantidad,
 (sum(precio_b) / count(1)) as precio_usd_promedio 
 from productos_ml.info_productos_ml where  fecha_proceso = current_date()
group by moneda_b
order by 2 desc;


-- Indica cantidad de envios gratis y cuantos no.
select 
 if(shipping_free=0,'No ofrece envios gratis','Envío gratis')as metodo_envio,
 count(1) as cantidad
from productos_ml.info_productos_ml where  fecha_proceso = current_date()
group by shipping_free
order by 1 desc;

-- Promedio con o sin garantia
select 
'Con garantía' as garantia,
round(count(a.id_ml) / (select count(1) from productos_ml.info_productos_ml where fecha_proceso = current_date()),2) porcentaje_con_garantia
from productos_ml.info_productos_ml a  where fecha_proceso = current_date()
and lower(a.garantia) !='sem garantia' 
and lower(a.garantia) !='sin garantia' 
and  a.garantia is not null
union
select 
'Sin garantía' as garantia,
round(count(a.id_ml) / (select count(1) from productos_ml.info_productos_ml),2) porcentaje_con_garantia
from productos_ml.info_productos_ml a where  fecha_proceso = current_date()
and (lower(a.garantia) ='sem garantia' 
or lower(a.garantia) ='sin garantia' 
or  a.garantia is null);