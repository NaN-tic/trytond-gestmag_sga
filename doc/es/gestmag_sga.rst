===========
Gestmag SGA
===========

Gestmag SGA permite la integración/comunicación de los datos del ERP con el SGA.

.. inheritref:: gestmag_sga/gestmag_sga:section:productos

---------
Productos
---------

Para exportar productos a Gestmag SGA:

* Al crear un producto nuevo, se genera un fichero CSV
* Al modificar un producto, se genera un fichero CSV
* Mediante la acción "Exportar productos a Gestmag SGA", se genera un fichero CSV por cada producto seleccionado.

.. inheritref:: gestmag_sga/gestmag_sga:section:albaranes_de_cliente

--------------------
Albaranes de cliente
--------------------

Se genera un fichero CSV cada vez que un albarán pase por el estado "Reserva".

.. important:: se genera el fichero cada vez que el albarán pasa por el estado "Reserva", por tanto,
               si el albarán se decide passar de empaquetado a reserva y volver a procesarlo,
               se generará un nuevo fichero con las modificaciones realizadas.

Al mismo tiempo, se genera un nuevo fichero CSV con los datos del cliente (nombre y dirección).

.. inheritref:: gestmag_sga/gestmag_sga:section:albaranes_de_proveedor

----------------------
Albaranes de proveedor
----------------------

Se genera un fichero CSV cada vez que un albarán pase por el estado "Recibido".

.. important:: se genera el fichero cada vez que el albarán pasa por el estado "Recibido", por tanto,
               si el albarán se decide passar de Recibido a borrador y se vuelve al estaod recibir,
               se generará un nuevo fichero con las modificaciones realizadas.

Al mismo tiempo, se genera un nuevo fichero CSV con los datos del proveedor (nombre y dirección).

.. inheritref:: gestmag_sga/gestmag_sga:section:configuracion

-------------
Configuración
-------------

A |menu_gestmag_configuration| configuraremos los directorios de importación/exportación de los ficheros

Estos directorios deberán tener permisos de escritura y serán los directorios que Gestmag tendrá montados.

.. |menu_gestmag_configuration| tryref:: gestmag_sga.menu_gestmag_configuration/complete_name
