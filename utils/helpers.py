from django.utils import timezone
from django.db.models import Q, Sum
from datetime import timedelta


def buscar_campos(model, campos, busqueda):
  modelo = model.objects.all()
  queries = []
  if busqueda:
    queries = [Q(**{campo + '__icontains': busqueda}) for campo in campos]
  if queries:
    query = queries.pop()
    for item in queries:
      query |= item
    modelo = modelo.filter(query).distinct()
  return modelo


def buscar_fecha(model, busquedaF):
  modelo = model.objects.all()
  query = Q(venta_FK__fecha_emision__icontains=busquedaF)
  modelo = modelo.filter(query).distinct()
  return modelo


def buscar_venta(model, campos, busqueda):
  modelo = model.objects.all()
  queries = []
  if busqueda is not None and busqueda.isdigit():
    busqueda = int(busqueda)
    for campo in campos:
      queries.append(Q(**{campo: busqueda}))
  elif busqueda:
    queries.append(Q(**{'venta_FK__usuario_FK__username': busqueda}))
  if queries:
    query = queries.pop()
    for item in queries:
      query |= item
    modelo = modelo.filter(query).distinct()
  return modelo


def total_dia(model, count_field, sum_field):
  today = timezone.now().date()  # fecha actual
  query = Q(venta_FK__fecha_emision__icontains=today)
  objects = model.objects.filter(query).distinct()
  count = objects.count()
  total = objects.aggregate(total=Sum(sum_field))['total']
  return {count_field: count, sum_field: total if total is not None else 0}


def total_ventas(boleta, periodo='semana'):
  ventas_totales = {}
  # Obtener la fecha actual
  now = timezone.localtime(timezone.now())
  # Crear un arreglo de fechas
  if periodo == 'dia':
    date_range = [now - timedelta(days=i) for i in range(6, -1, -1)]
  elif periodo == 'semana':
    date_range = [now - timedelta(weeks=i) for i in range(6, -1, -1)]
  elif periodo == 'mes':
    date_range = [now - timedelta(days=30 * i) for i in range(6, -1, -1)]
  else:
    raise ValueError("El periodo debe ser 'dia', 'semana' o 'mes'")
  # Calcular el total de ventas para cada día en el rango
  for date in date_range:
    if periodo == 'dia':
        # Filtrar Boletas por el rango de fecha del día
      start_time = timezone.make_aware(
          timezone.datetime(date.year, date.month, date.day, 0, 0, 0)
      )
      end_time = timezone.make_aware(
          timezone.datetime(
              date.year,
              date.month,
              date.day,
              23,
              59,
              59,
              999999)
      )
      query = Q(venta_FK__fecha_emision__range=(start_time, end_time))
    elif periodo == 'semana':
      # Calcular el primer día (hace 7 días) y el último día (hoy)
      first_day = date - timedelta(weeks=1)
      last_day = date
      query = Q(venta_FK__fecha_emision__range=(first_day, last_day))
    elif periodo == 'mes':
      # Calcular el primer día y el último día del mes
      first_day = date.replace(day=1)
      if first_day.month == 12:
        last_day = first_day.replace(
            year=first_day.year + 1, month=1, day=1) - timedelta(days=1)
      else:
        last_day = first_day.replace(
            month=first_day.month + 1, day=1) - timedelta(days=1)
      query = Q(venta_FK__fecha_emision__range=(first_day, last_day))

    objects_boletas = boleta.objects.filter(query).distinct()
    total_boletas = objects_boletas.aggregate(
        total=Sum('total_boleta'))['total'] or 0
    ventas_totales[date.strftime("%Y-%m-%d")] = total_boletas

  return ventas_totales


def top_productos(model_productos, model_detalle, campos_producto):
  # Calcular la fecha de hace 30 días desde la fecha actual
  fecha_hace_30_dias = timezone.localtime(timezone.now()) - timedelta(days=30)

  # Obtener todos los productos
  productos_no_en_boletas = model_productos.objects.exclude(
      detalleboletas__isnull=False).values(*campos_producto)

  # Agrega el prefijo 'producto_FK__' a cada campo en la lista campos_producto
  campos_producto_con_prefijo = [
      'producto_FK__' +
      campo for campo in campos_producto]

  # Obtener los productos más vendidos de DetalleBoletas
  productos_boletas = model_detalle.objects.filter(
      boleta_FK__venta_FK__fecha_emision__gte=fecha_hace_30_dias
  ).values(*campos_producto_con_prefijo)

  productos_boletas = productos_boletas.annotate(
      total_vendido=Sum('cantidad'))

  # Unir los resultados de ambas consultas utilizando un left join y ordenar
  top_mas_vendidos = productos_boletas.order_by('-total_vendido')[:10]

  top_menos_vendidos_boleta = productos_boletas.order_by('total_vendido')[:10]

  # Convierte las consultas en listas
  productos_no_en_boletas_lista = list(productos_no_en_boletas)
  top_menos_vendidos_lista = list(top_menos_vendidos_boleta)

  # Combina las dos listas
  productos_combinados = productos_no_en_boletas_lista + top_menos_vendidos_lista

  # Toma los primeros 10 elementos de la lista combinada
  top_menos_vendidos = productos_combinados[:10]

  return top_mas_vendidos, top_menos_vendidos


def buscar_fecha_rango(modal, fecha1, fecha2, periodo):
  pass


def generar_pdf(queryset, camposH, camposB):
  pass
