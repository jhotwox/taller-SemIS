# Tkinter
from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, StringVar, CTkOptionMenu as OptMenu
from tkinter import messagebox, Spinbox
from tkcalendar import Calendar
# SQL and extra functions
from functions import entry_empty, clean_str, find_id, get_date, get_datetime, format_date_to_sql, format_date_to_calendar
from db_functions import license_plate_available, available_license_plates, available_parts, search_parts, all_parts, license_plate_on_repair
from repair import repair as repair_class
from repair_part import repair_part as repair_part_class
from part import part as part_class
from db_repair import db_repair
from db_repair_part import db_repair_part
from db_part import db_part
# Time
from datetime import datetime, timedelta

# Profile
from user import user as user_class

# TODO:
# Modicar que al guardar y editar se compruebe la cantidad de piezas en stock
# Actualizar las piezas de los opm en los default

class Repairs:
    
    def __init__(self, profile: user_class):
        self.profile = profile
        self.band = None
        self.max_quantity = None
        self.quantity_edit = None
        self.part_id_edit = None
        self.replace_stock = None
        self.new_date = None
        self.all_part: dict = all_parts()
        self.window = CTk()
        self.window.title("Reparaciones")
        self.window.config(width=400, height=400)

        fr_search = Frame(self.window)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=5)
        fr_entry = Frame(self.window)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=5)
        fr_button = Frame(self.window)
        fr_button.grid(row=2, column=0, sticky="nsw", padx=10, pady=5)
        
        self.lb_search_folio = Label(fr_search, text="Folio a buscar: ", font=("Calisto MT", 12))
        self.lb_search_folio.grid(row=0, column=0, padx=5)
        self.tx_search_folio = Entry(fr_search, placeholder_text="Folio a buscar", width=140)
        self.tx_search_folio.grid(row=0, column=1,  padx=10, pady=10)
        self.bt_search_folio = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_part)
        self.bt_search_folio.grid(row=0, column=2, padx=5, pady=10)
        
        self.lb_search_part = Label(fr_search, text="Pieza a buscar: ", font=("Calisto MT", 12))
        self.lb_search_part.grid(row=1, column=0, padx=5)
        self.search_parts = {}
        self.selected_search_part = StringVar(value="No disponible")
        self.opm_search_part = OptMenu(fr_search, values=list(self.search_parts.values()), variable=self.selected_search_part)
        self.opm_search_part.grid(row=1, column=1, pady=5)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_repair)
        self.bt_search.grid(row=1, column=2, padx=5, pady=10)

        self.lb_folio = Label(fr_entry, text="Folio")
        self.lb_folio.grid(row=0, column=0, pady=0)
        self.tx_folio = Entry(fr_entry, placeholder_text="Folio")
        self.tx_folio.grid(row=0, column=1, pady=5)

        self.license_plates: list = available_license_plates(profile.get_id())
        self.lb_license_plate = Label(fr_entry, text="Matricula")
        self.lb_license_plate.grid(row=1, column=0, pady=0)
        self.selected_license_plate = StringVar(value=self.license_plates[0] if len(self.license_plates) > 0 else "No disponible")
        self.selected_license_plate.trace("w", self.on_selection_license_plate)
        self.opm_license_plate = OptMenu(fr_entry, values=list(self.license_plates), variable=self.selected_license_plate)
        self.opm_license_plate.grid(row=1, column=1, pady=5)
        
        self.parts: dict = available_parts()
        self.lb_part = Label(fr_entry, text="Pieza")
        self.lb_part.grid(row=2, column=0, pady=0)
        self.selected_part = StringVar(value=next(iter(self.parts.values())) if len(self.parts) > 0 else "No disponible")
        self.selected_part.trace("w", self.on_selection_part)
        self.opm_part = OptMenu(fr_entry, values=list(self.parts.values()), variable=self.selected_part)
        self.opm_part.grid(row=2, column=1, pady=5)
        
        self.lb_quantity = Label(fr_entry, text="Cantidad")
        self.lb_quantity.grid(row=3, column=0, pady=0)
        self.sp_quantity = Spinbox(fr_entry, from_=0, to=10, width=15, fg="#000", buttonbackground="#1F6AA5", buttoncursor="hand2")
        self.sp_quantity.grid(row=3, column=1, pady=5, padx=20)
        
        self.lb_fault = Label(fr_entry, text="Fallo")
        self.lb_fault.grid(row=4, column=0, pady=0)
        self.tx_fault = Entry(fr_entry, placeholder_text="Fallo")
        self.tx_fault.grid(row=4, column=1, pady=5, padx=20)
        
        [day_in, month_in, year_in] = get_date()
        [day_out, month_out, year_out] = get_date(2)
        
        self.lb_date_in = Label(fr_entry, text="Fecha\nentrada")
        self.lb_date_in.grid(row=5, column=0, pady=0)
        self.cal_date_in = Calendar(fr_entry, selectmode="day", year=int(year_in), month=int(month_in), day=int(day_in))
        self.cal_date_in.grid(row=5, column=1, pady=5, padx=20)
        
        self.lb_date_out = Label(fr_entry, text="Fecha\nsalida")
        self.lb_date_out.grid(row=6, column=0, pady=0)
        self.cal_date_out = Calendar(fr_entry, selectmode="day", year=int(year_out), month=int(month_out), day=int(day_out))
        self.cal_date_out.grid(row=6, column=1, pady=5, padx=20)

        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_repair)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_repair)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_repair)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_repair)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        
        self.default()
        
        self.window.mainloop()
    
    def on_selection_part(self, *args):
        # En caso de que deseemos editar algo sin stock

        aux = part_class(id=find_id(self.all_part, self.selected_part.get()))
        part = db_part.search(self, aux)
        # Editar
        if not self.band:
            if self.part_id_edit == find_id(self.all_part, self.selected_part.get()):
                self.max_quantity = part.get_stock() + self.quantity_edit
                return
            else:
                # significa que vamos a reestablecer el stock de la otra pieza
                self.replace_stock = True
        # Guardar o es otra pieza
        self.max_quantity = part.get_stock()
    
        # Actualizar cantidad maxima
        self.sp_quantity.configure(from_=0, to=self.max_quantity)
    
    def on_selection_license_plate(self, *args):
        self.tx_folio.configure(state=ENABLE)
        folio = license_plate_on_repair(self.selected_license_plate.get())
        self.tx_folio.delete(0, END)
        if folio > 0:
            self.tx_folio.insert(0, folio)
            self.new_date = False

            repair = db_repair.search(self, repair_class(folio=folio))
            # print(f"Format time: {repair.get_date_in()}")
            self.cal_date_in.selection_set(format_date_to_calendar(str(repair.get_date_in())))
            self.cal_date_out.selection_set(format_date_to_calendar(str(repair.get_date_out())))
            self.cal_date_in.configure(state=DISABLED)
            self.cal_date_out.configure(state=DISABLED)
        else:
            self.tx_folio.insert(0, db_repair.get_max_folio(self)+1)
            self.new_date = True

            # Agregar fecha del dia de hoy
            self.cal_date_in.configure(state=ENABLE)
            self.cal_date_out.configure(state=ENABLE)
        self.tx_folio.configure(state=DISABLED)

    def search_part(self) -> None:
        self.search_parts = search_parts(self.tx_search_folio.get())
        if self.search_parts is None or self.search_parts == {}:
            self.opm_search_part.configure(state=DISABLED)
            self.bt_search.configure(state=DISABLED)
            messagebox.showwarning("Error", "No se encontraron partes")
            return
        self.opm_search_part.configure(state=ENABLE)
        self.opm_search_part.configure(values=list(self.search_parts.values()))
        self.opm_search_part.set(next(iter(self.search_parts.values())))
        self.bt_search.configure(state=ENABLE)
    
    def search_repair(self, loop: int = 1) -> None:
        if not self.tx_search_folio.get().isdecimal():
            messagebox.showwarning("Error", "Ingrese un folio válido")
            return

        repair_part_id = find_id(self.search_parts, self.opm_search_part.get())
        aux = repair_class(folio=self.tx_search_folio.get())
        repair = db_repair.search(self, aux)
        
        aux = repair_part_class(folio=self.tx_search_folio.get(), part_id=repair_part_id)
        # print("I'm here")
        repair_part = db_repair_part.search(self, aux)
        
        
        if repair is None or repair_part is None:
            return

        self.enable_search()
        self.tx_folio.insert(0, repair.get_folio())
        self.tx_folio.configure(state=DISABLED)

        self.opm_license_plate.set(repair.get_license_plate())
        self.opm_part.set(self.all_part[repair_part.get_part_id()])
        self.sp_quantity.insert(0, str(repair_part.get_quantity()))
        self.sp_quantity.configure(state='readonly')
        self.tx_fault.insert(0, repair_part.get_fault())
        date_in = format_date_to_calendar(str(repair.get_date_in()))
        date_out = format_date_to_calendar(str(repair.get_date_out()))
        print(f"Search date in -> {date_in}")
        print(f"Search date out -> {date_out}")
        self.cal_date_in.selection_set(date_in)
        self.cal_date_out.selection_set(date_out)
        
        self.quantity_edit = repair_part.get_quantity()
        self.part_id_edit = repair_part.get_part_id()
        
        # Soluciona el error de que se necesita buscar por segunda vez para actualizar correctamente la cantidad en el spinbox
        if loop == 1:
            self.search_repair(0)

    def new_repair(self) -> None:
        self.tx_folio.configure(state=ENABLE)
        self.opm_license_plate.configure(state=ENABLE)
        self.opm_part.configure(state=ENABLE)
        self.sp_quantity.configure(state='normal')
        self.tx_fault.configure(state=ENABLE)
        self.cal_date_in.configure(state=ENABLE)
        self.cal_date_out.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_repair()
        self.tx_folio.insert(0, db_repair.get_max_folio(self)+1)
        self.tx_folio.configure(state=DISABLED)
        self.sp_quantity.configure(state='readonly')
        self.band = True

    def save_repair(self) -> None:            
        try:
            # Validar fechas validas
            self.validate()
        except Exception as error:
            messagebox.showwarning("save_repair_error", error)
            return

        # Comprobar si se necesita state normal en spinbox (Parece que no es necesario)
        folio = clean_str(self.tx_folio.get())
        license_plate = clean_str(self.opm_license_plate.get())
        clean_part = clean_str(self.opm_part.get())
        quantity = clean_str(self.sp_quantity.get())
        fault = clean_str(self.tx_fault.get())
        
        try:
            # ID de la nueva parte
            part_id = find_id(self.all_part, clean_part)
            # Añador a la instancia repair la fecha de entrada y salida si se esta editando o creando una nueva reparacion con un vehiculo (matricula)nuevo
            # No es necesario guardar una instancia de repair si el vehiculo ya esta en la tabla de reparaciones
            # if self.new_date == True or self.band == False:
            #     repair: repair_class = repair_class(int(folio), license_plate, self.cal_date_in.get_date(), self.cal_date_in.get_date())
            if self.new_date == True or self.band == False:
                date_in = format_date_to_sql(self.cal_date_in.get_date())
                date_out = format_date_to_sql(self.cal_date_out.get_date())
                repair: repair_class = repair_class(int(folio), license_plate, date_in, date_out)
            
            repair_part: repair_part_class = repair_part_class(int(folio), part_id, int(quantity), fault)

            print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            print(f"{"Saving" if self.band else 'editing'} repair\n")
            print(f"part -> {clean_part}")
            print(f"part_id -> {part_id}")

            # Parte seleccionada del opm: no es pieza a reponer
            aux: part_class = part_class(id=part_id)
            part = db_part.search(self, aux)

            if self.band == True:
                # Aun no se agrega el vehiculo a folio
                # TODO: Puede que esta validación solo necesite self.new_date en lugar de la consulta a la BD
                if license_plate_on_repair(self.selected_license_plate.get()) == 0:
                    db_repair.save(self, repair)
                db_repair_part.save(self, repair_part)

                # REDUCIR STOCK
                stock = part.get_stock() - int(self.sp_quantity.get())
                print("Part Stock before -> ", part.get_stock())
                print("Part Stock after -> ", stock)
                new_part: part_class = part_class(id=part_id, stock=stock)
                db_part.edit_stock(self, new_part)

                messagebox.showinfo("Exitoso", "Parte guardada exitosamente!")
            else:
                db_repair.edit(self, repair)
                db_repair_part.edit(self, repair_part)

                # Otra pieza
                if self.replace_stock:
                    # REPONER STOCK VIEJA PIEZA
                    aux = db_part.search(self, part_class(id=self.part_id_edit))
                    old_part = part_class(id=self.part_id_edit, stock=aux.get_stock() + self.quantity_edit)
                    replace_stock = db_part.edit_stock(self, old_part)
                    print(f"Old part stock before -> {aux.get_stock()}")
                    print(f"Old part stock after -> {replace_stock.get_stock()}")
                    # REDUCIR STOCK NUEVA PIEZA
                    # new_part = part_class(id=part_id)
                    # new_part = db_part.search(self, new_part)
                    db_part.edit_stock(self, part_class(id=part_id, stock=part.get_stock() - int(self.sp_quantity.get())))
                    print(f"New part stock before -> {part.get_stock()}")
                    print(f"New part stock afer -> {part.get_stock() - int(self.sp_quantity.get())}")

                # Misma pieza
                else:
                    # CAMBIAR STOCK
                    # stock = teniamos 4 - ahora son 6 = -2
                    # stock = teniamos 4 - ahora son 3 = 1
                    print("Quantity edit")
                    print(f"Same part stock before -> {self.quantity_edit}")
                    stock = self.quantity_edit - self.sp_quantity.get()
                    print(3)
                    # stock = el stock actual es de 3 + (-2) = 1
                    # stock = el stock actual es de 3 + 1 = 4
                    stock = part.get_stock() + stock
                    print("Same part stock after -> ", stock)
                    new_part = part_class(id=self.part_id_edit, stock=stock)
                db_part.edit_stock(self, new_part)
                
                messagebox.showinfo("Exitoso", "Parte editada exitosamente!")
                
            self.default()
        except Exception as err:
            print(f"[-] save_repair: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} pieza en BD")
        finally:
            self.band = None
            self.new_date = None
            self.quantity_edit = None

    def remove_repair(self) -> None:
        self.tx_folio.configure(state=ENABLE)
        
        try:
            aux = repair_class(folio=self.tx_folio.get())
            self.tx_folio.configure(state=DISABLED)
            db_repair.remove(self, aux)
            self.default()
            messagebox.showinfo("Exitoso", "Reparación eliminada exitosamente!")
        except Exception as err:
            print(f"[-] remove_repair: {err}")
            messagebox.showerror("Error", "No se logro eliminar la reparación")
        
    def edit_repair(self) -> None:
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_remove.configure(state=DISABLED)
        self.band = False
    
    def clear_repair(self):
        self.tx_folio.delete(0, END)
        self.opm_license_plate.configure(values=self.license_plates)
        self.opm_license_plate.set(self.license_plates[0] if len(self.license_plates) > 0 else "No disponible")
        self.opm_part.configure(values=list(self.parts.values()))
        self.opm_part.set(next(iter(self.parts.values())) if len(self.parts) > 0 else "No disponible")
        self.tx_fault.delete(0, END)
        self.sp_quantity.delete(0, END)
        
        self.cal_date_in.selection_set(get_datetime())
        self.cal_date_out.selection_set(get_datetime(2))
    
    #region default
    def default(self):
        # Update list of license plates
        self.license_plates = available_license_plates(self.profile.get_id())
        
        self.cal_date_in.configure(state=ENABLE)
        self.cal_date_out.configure(state=ENABLE)
        self.tx_folio.configure(state=ENABLE)
        self.opm_license_plate.configure(state=ENABLE)
        self.opm_part.configure(state=ENABLE)
        self.sp_quantity.configure(state='normal')
        self.tx_fault.configure(state=ENABLE)
        self.clear_repair()
        
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_folio.configure(state=DISABLED)
        self.opm_license_plate.configure(state=DISABLED)
        self.opm_part.configure(state=DISABLED)
        self.sp_quantity.configure(state="disabled")
        self.tx_fault.configure(state=DISABLED)
        self.cal_date_in.configure(state=DISABLED)
        self.cal_date_out.configure(state=DISABLED)
        
        self.opm_search_part.configure(state=DISABLED)
        self.bt_search.configure(state=DISABLED)
    
    #region enable_search
    def enable_search(self):
        if self.profile.get_profile() == "admin":
            self.bt_new.configure(state=DISABLED)
            self.bt_save.configure(state=DISABLED)
            self.bt_cancel.configure(state=ENABLE)
            self.bt_edit.configure(state=ENABLE)
            self.bt_remove.configure(state=ENABLE)
        else:
            self.bt_new.configure(state=DISABLED)
            self.bt_save.configure(state=DISABLED)
            self.bt_cancel.configure(state=ENABLE)
            self.bt_edit.configure(state=DISABLED)
            self.bt_remove.configure(state=DISABLED)

        self.tx_folio.configure(state=ENABLE)
        self.opm_license_plate.configure(state=ENABLE)
        self.opm_part.configure(state=ENABLE)
        self.sp_quantity.configure(state='normal')
        self.tx_fault.configure(state=ENABLE)
        self.cal_date_in.configure(state=ENABLE)
        self.cal_date_out.configure(state=ENABLE)
        self.clear_repair()

    #region Validate
    def validate(self) -> None:
        entry_empty(self.tx_folio, "Folio")
        entry_empty(self.opm_license_plate, "Matricula")
        entry_empty(self.opm_part, "Parte")
        entry_empty(self.sp_quantity, "Cantidad")
        entry_empty(self.tx_fault, "Fallo")

        # print(f"ID encontrado -> {find_id(self.all_part, self.opm_part.get())}")
        repair_part = repair_part_class(folio=self.tx_folio.get(), part_id=find_id(self.all_part, self.opm_part.get()))
        if db_repair_part.search_bool(self, repair_part):
            raise Exception("Ya existe una reparación con ese folio y parte")

        if self.opm_license_plate.get() == "No disponible":
            raise Exception("No se encontraron vehiculos")
        
        if self.opm_part.get() == "No disponible":
            raise Exception("No se encontraron partes")

        if not self.tx_folio.get().isdecimal():
            raise Exception("Folio no valido")
        
        if not self.sp_quantity.get().isdecimal():
            raise Exception("Cantidad debe ser un número entero")

        if len(self.sp_quantity.get()) > 10:
            raise Exception("Tamaño maximo de cantidad: 10 caracteres")

        if len(self.tx_fault.get()) > 80:
            raise Exception("Tamaño maximo de fallo: 80 caracteres")

        date_in = datetime.strptime(self.cal_date_in.get_date(), "%d/%m/%y")
        date_out = datetime.strptime(self.cal_date_out.get_date(), "%d/%m/%y")
        if  date_in > date_out:
            raise Exception("Las fechas no coinciden")

        self.validate_license_plate(self.opm_license_plate.get())

    def validate_license_plate(self, license: str) -> None:
        if not (6 <= len(license) <= 7):
            raise Exception("La matricula debe contener 6 o 7 caracteres")
