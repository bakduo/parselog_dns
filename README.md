Parselog DNS
======================

En este apartado se presenta una primera solución para poder extraer información sobre:


- direcciones ip.
- contador total agrupdo por rangos de red.
- cantidad de peticiones con timeout.
- cantidad de peticiones totales.
- etc.


Actualmente están implementadas tres funcionalidades:

- Generación de reporte por ip y contabilizar rangos de subredes por parámetros.
- Generación de reporte cantidad de consultas que generan timeout.
- Generación de reporte por cantidad de solicitudes que ha generado NXDOMAIN.


Esto puede resultar útil en caso de tener una muestra de información además de los monitor de prometheus + grafana. En vista que en general existen ataques de DNS en formato wildcard y nos ayuda a tener información al respecto.


# Ejemplo de uso

Este parser esta orientado y basado en el uso de la herramienta coredns. Por lo tanto necesitan tener el plugin de **log** habilitado.

Ejemplo:

```
[INFO] z.x.x.x:64486 - 12403 "AAAA IN sitio.com. udp 72 false 512" NXDOMAIN qr,aa,rd 173 0.000373973s
[INFO] z.x.x.x:57117 - 55876 "A IN sitio2.com. udp 92 false 512" NXDOMAIN qr,aa,rd 193 0.000252328s
[INFO] z.x.x.x:57117 - 89 "AAAA IN sitio3.com. udp 92 false 512" NXDOMAIN qr,aa,rd 193 0.000441813s

```

Rango de redes del cual queremos tener información para exportar:

```
SUBNET=['192.168.x.0',
        '192.168.x.0',
        '192.168.x.0']

```

Actualmente, no hace falta agregar **/24** ya que solo soporta clientes de clase C.
