TODO:
- Buscar por nombre
- Asegurarse de si debemos de modificar solo los clientes que nosotros registramos
- Asegurarse de si debemos de modificar solo los vehiculos que nosotros registramos
- Poder regresar a ventana menu
    - https://noobtomaster.com/python-gui-tkinter/building-multi-window-applications-and-navigation/
- Ingreso correcto de fecha
- No se actualiza la fecha al buscar
- No se coloca el spinbox en readonly al buscar

COMPLETE:
- Guardar reparación con nueva matricula
- Guardar reparación con matricula ya registrada



Solucionar error:
- Despues de buscar un pruducto cambiar el folio sin presionar buscar
- Solucion: Despues de cada busqueda de pieza desactivar el boton de busqueda de pieza hasta que se vuelva a buscar el folio
    [-] search in db_repair_part: 'NoneType' object is not subscriptable
    Exception in Tkinter callback
    Traceback (most recent call last):
    File "/home/jhodox/Documents/codigo/python/semIngSoftware/taller/db_repair_part.py", line 40, in search
        if row[0] is not None:
        ~~~^^^
    TypeError: 'NoneType' object is not subscriptable

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
    File "/usr/lib/python3.12/tkinter/__init__.py", line 1968, in __call__
        return self.func(*args)
            ^^^^^^^^^^^^^^^^
    File "/usr/lib/python3.12/site-packages/customtkinter/windows/widgets/ctk_button.py", line 554, in _clicked
        self._command()
    File "/home/jhodox/Documents/codigo/python/semIngSoftware/taller/repairs.py", line 186, in search_repair
        repair_part = db_repair_part.search(self, aux)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/jhodox/Documents/codigo/python/semIngSoftware/taller/db_repair_part.py", line 44, in search
        raise Exception(f"No se encontro el folio - parte")
    Exception: No se encontro el folio - parte