# Import de las librerías necesarias para hacer el proyecto
import requests
import mysql.connector
from mysql.connector import cursor
from datetime import datetime

class productos():

    def __init__(self) -> None:
        print("")

# Busco los atributos de los productos en /items/
    def busca_atributos(self, idml):
        BD = BaseDatos()
        url_items="https://api.mercadolibre.com/items/"
        url_name = url_items + idml
		
        #registro en bd inicio ejecucion api items productos
        sql = "insert into productos_ml.info_producto_log (fecha_inicio, nombre_api, status_proc) values (now(), 'api items productos', 'Ejecutando')"
        BD.query_log(sql)
        response = requests.get(url_name)

        if response.status_code == 200:
            #registro en bd fin ejecucion api items productos
            sql = "update productos_ml.info_producto_log set status_proc='Finalizado', fecha_fin = now(), duracion = round(time_to_sec(fecha_fin)-time_to_sec(fecha_inicio),60) where fecha_inicio>=current_date() and nombre_api ='api items productos' and fecha_fin is null"
            BD.query_log(sql)
            datos = response.json()
            return datos

####################################################################################################
class BaseDatos():
# Creo la conexión a la base de datos mysql
    def bd_conexion():
        dbcone = {
                'host': '127.0.0.1',
                'user': 'cbrito20',
                'password': 'Rtbs201-_$$',
                'db': 'productos_ml'
                }
        conexion = mysql.connector.connect(**dbcone)        
        return conexion

#  Uso esta función para registrar en base de datos los kpi de ejecución
    def query_log(self, sql):
        conec = BaseDatos.bd_conexion()
        cursor = conec.cursor()
        cursor.execute (sql)
        conec.commit()
        conec.close()

#  Uso esta función para insert en la tabla principal 
    def query_proceso(self, sql, var):
        conec = BaseDatos.bd_conexion()
        cursor = conec.cursor()
        cursor.execute (sql, var)
        conec.commit()
        print(cursor.rowcount, "Registros procesados")
        conec.close()

 ####################################################################################################   
#  Uso esta función para Buscar las garantías de los productos
def busca_garantia(garant):
    for ga in garant:
        xa = ga['values']
        for xb in xa:
            x= (xb['name'])
            # Vienen otros registros, entonces filtro los datos
            no_aplica=("garantia do vendedor",  "garantía del vendedor", "garantía de fábrica")
            if x.lower() not in no_aplica:
                #print(x)
                return x
####################################################################################################
# Busco la condición de los productos, 
def condicion_prod(atri_1):
    for a in atri_1:
        b = a['value_name']
        # filtro porque vienen otros valores
        if b.lower() in ("nuevo", "novo", "reacondicionado", "usado", "used", "new", "recondicionado"):
            ##print(b)
            return b
			
####################################################################################################
# Busco condición del producto, esta es una segunda parte
def condicion_prod_2(atri_2):

    if atri_2.lower() in ("new", "nuevo"):
        cond_2 = atri_2
        return cond_2.lower()
		
####################################################################################################
# Funcion para buscar las ventas en la api
def get_ventas(seller):
    BD=BaseDatos()
    url_user = "https://api.mercadolibre.com/users/"
    url_ventas = url_user + str(seller)
    #registro en bd inicio ejecucion api busca ventas
    sql = "insert into productos_ml.info_producto_log (fecha_inicio, nombre_api, status_proc) values (now(), 'api busca ventas', 'Ejecutando')"
    BD.query_log(sql)
    ventas = requests.get(url_ventas)

    if ventas.status_code == 200:
        #registro en bd fin ejecucion api busca ventas
        sql = "update productos_ml.info_producto_log set status_proc='Finalizado', fecha_fin = now(), duracion = round(time_to_sec(fecha_fin)-time_to_sec(fecha_inicio),60) where fecha_inicio>=current_date() and nombre_api ='api busca ventas' and fecha_fin is null"
        BD.query_log(sql)
        data = ventas.json()
        vtas_cancel=  data['seller_reputation']['transactions']['canceled']
        vtas_complet= data['seller_reputation']['transactions']['completed']
        total_vtas=   data['seller_reputation']['transactions']['total']
        
        return (vtas_cancel, vtas_complet, total_vtas)

####################################################################################################
# Función para haccer la conversión de monedas
def conversion_brl_to_usd(valor_ars):
    BD=BaseDatos()
    conversion="https://api.mercadolibre.com/currency_conversions/search?from=BRL&to=USD"
    #registro en bd inicio ejecucion api conversion moneda
    sql = "insert into productos_ml.info_producto_log (fecha_inicio, nombre_api, status_proc) values (now(), 'api conversion moneda', 'Ejecutando')"
    BD.query_log(sql)
    response = requests.get(conversion)

    if response.status_code == 200:
        #registro en bd fin ejecucion api conversion moneda
        sql = "update productos_ml.info_producto_log set status_proc='Finalizado', fecha_fin = now(), duracion = round(time_to_sec(fecha_fin)-time_to_sec(fecha_inicio),60) where fecha_inicio>=current_date() and nombre_api ='api conversion moneda' and fecha_fin is null"
        BD.query_log(sql)
        
        dat = response.json()
        moneda = dat['currency_quote']
        fecha_vigencia =  dat['valid_until'][0:10]
        valor_conversion = dat['inv_rate']
        # Si llegamos a obtner un precio con valor 0 se retornará cero.
        if valor_ars <= 0:
            valor_usd= 0
        else:
         valor_usd = valor_ars / valor_conversion
        return (round(valor_usd,2), moneda, fecha_vigencia)

##############################################################################################
# Se procede a buscar los id_de las publicaciones para proceder a extraer los atributos
def get_atributos_prod():
    BD=BaseDatos()
    bp=productos()

    #registro en bd inicio ejecucion api search productos
    sql = "insert into productos_ml.info_producto_log (fecha_inicio, nombre_api, status_proc) values (now(), 'api search productos', 'Ejecutando')"
    BD.query_log(sql)
    url_search="https://api.mercadolibre.com/sites/MLB/search?q="
    producto= "Samsung Galaxy A20"
    offset = "&offset="
    #La API devuelve un limite de 50 ID'S. Por el metodo offset lo incremeto para poder traerme los requeridos
    limit = 50
    #registro en bd fin ejecucion api search productos
    sql = "update productos_ml.info_producto_log set status_proc='Finalizado', fecha_fin = now(), duracion = round(time_to_sec(fecha_fin)-time_to_sec(fecha_inicio),60) where fecha_inicio>=current_date() and nombre_api ='api search productos' and fecha_fin is null"
    BD.query_log(sql)

    while limit <=210:
        url_name = url_search + producto + offset + str(limit)                       
        resp = requests.get(url_name)
        limit= limit+50
                   
        if resp.status_code == 200:
            data = resp.json() 
    
            for x in data['results']:
                id_ml = x['id']    
# Procedo a extraer los atributos en la API
                valores = bp.busca_atributos(id_ml) 

                cond_a= condicion_prod(valores['attributes']) 
                cond_b= valores['condition']
                #id_ml 
                seller = valores['seller_id']
                title = valores['title']
                precio_a = valores['price']
                moneda_a = valores['currency_id']     
                conver = conversion_brl_to_usd(valores['price'])
                precio_b = conver[0]
                moneda_b = conver[1]
                fecha_v = conver[2]
                #cond_a
                #cond_b
                garantia = busca_garantia(valores['sale_terms'])
                envio = valores['shipping']['free_shipping'] 
                ventas = get_ventas(valores['seller_id'])
                vtas_cancel = ventas[0]
                vtas_complet = ventas[1]
                total_vtas = ventas[2]
                url_ml = valores['permalink']
                
                #Otengo la fecha del proceso
                fecha_proceso = datetime.now().strftime('%Y-%m-%d')
                
                #Armo una lista para proceder a realizar el insert en la tabla principal
                var = (fecha_proceso, id_ml, seller,
                title, precio_a, moneda_a,
                precio_b, moneda_b, fecha_v,
                cond_a, cond_b, garantia, 
                envio, vtas_cancel, vtas_complet,
                total_vtas, url_ml)

                #Registra tiempo de insert a la base
                sql = "insert into productos_ml.info_producto_log (fecha_inicio, nombre_api, status_proc) values (now(), 'Carga tabla principal', 'Ejecutando')"
                BD.query_log(sql)

# Inserta registros en la  tabla principal de mysql
                sql= "insert into productos_ml.info_productos_ml (fecha_proceso,id_ml,seller_id,titulo_producto,precio_a, moneda_a, precio_b, moneda_b, fecha_valida_conversion, condicion_prod_1,condicion_prod_2,garantia,shipping_free,total_vtas_canceladas,total_vtas_completas,total_vtas,url_producto) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                BD.query_proceso(sql, var)
                
                #Actualiza tiempo de carga del registro
                sql = "update productos_ml.info_producto_log set status_proc='Finalizado', fecha_fin = now(), duracion = round(time_to_sec(fecha_fin)-time_to_sec(fecha_inicio),60) where fecha_inicio>=current_date() and nombre_api ='Carga tabla principal' and fecha_fin is null"
                BD.query_log(sql)
    
####################################################################################################              
 # Función que llama al metodo principal                                          
if __name__ == '__main__':
    qr = BaseDatos()
    # Registra inicio del proceso 
    sql = "insert into productos_ml.info_producto_log (fecha_inicio, nombre_api, status_proc) values (now(), 'Proceso productos', 'Ejecutando')"
    qr.query_log(sql)

# Si se reejecuta el proceso en el mismo día NO duplicamos registros.
    sql= "delete  from productos_ml.info_productos_ml where fecha_proceso >= current_date"
    qr.query_log(sql)
    # Se invoca a la funcion principal
    get_atributos_prod()

# Registro en bd fin ejecucion
    sql = "update productos_ml.info_producto_log set status_proc='Finalizado', fecha_fin = now(), duracion = round(time_to_sec(fecha_fin)-time_to_sec(fecha_inicio),60) where fecha_inicio>=current_date() and nombre_api ='Proceso productos' and fecha_fin is null"
    qr.query_log(sql)