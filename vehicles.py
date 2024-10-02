from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, StringVar, CTkOptionMenu as OptMenu
from tkinter import messagebox
from functions import entry_empty, is_alphabetic, clean_str, find_id
from db_functions import available_customers, name_by_id, license_plate_available
from vehicle import vehicle as vehicle_class
from db_vehicle import db_vehicle
from user import user as user_class

class Vehicles:
    def __init__(self, profile: user_class):
        self.profile = profile
        self.band = None
        self.window = CTk()
        self.window.title("Vehiculos")
        self.window.config(width=400, height=400)
        
        fr_search = Frame(self.window)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_entry = Frame(self.window)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        fr_button = Frame(self.window)
        fr_button.grid(row=2, column=0, sticky="nsw", padx=10, pady=10)
        
        self.lb_search = Label(fr_search, text="Matricula a buscar: ", font=("Calisto MT", 12))
        self.lb_search.grid(row=0, column=0, padx=5)
        self.tx_search = Entry(fr_search, placeholder_text="Matricula a buscar", width=200)
        self.tx_search.grid(row=0, column=1,  padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_vehicle)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        
        self.lb_license_plate = Label(fr_entry, text="Matricula")
        self.lb_license_plate.grid(row=0, column=0, pady=0)
        self.tx_license_plate = Entry(fr_entry, placeholder_text="Matricula")
        self.tx_license_plate.grid(row=0, column=1, pady=5)

        self.customers = available_customers(profile.get_id())
        self.lb_customer_name = Label(fr_entry, text="Cliente")
        self.lb_customer_name.grid(row=1, column=0, pady=0)
        self.selected_customer = StringVar(value=next(iter(self.customers.values())) if len(self.customers) > 0 else "No disponible")
        # print(f"LLaves: {self.customers.keys()}")
        # print(f"Valores: {self.customers.values()}")
        self.opm_customer_name = OptMenu(fr_entry, values=list(self.customers.values()), variable=self.selected_customer)
        self.opm_customer_name.grid(row=1, column=1, pady=5)
        
        self.lb_model = Label(fr_entry, text="Modelo")
        self.lb_model.grid(row=2, column=0, pady=0)
        self.tx_model = Entry(fr_entry, placeholder_text="Modelo")
        self.tx_model.grid(row=2, column=1, pady=5, padx=20)
        
        self.lb_brand = Label(fr_entry, text="Marca")
        self.lb_brand.grid(row=3, column=0, pady=0)
        self.tx_brand = Entry(fr_entry, placeholder_text="Marca")
        self.tx_brand.grid(row=3, column=1, pady=5, padx=20)


        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_vehicle)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_vehicle)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_vehicle)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_vehicle)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        
        self.default()
        
        self.window.mainloop()
    
    def search_vehicle(self) -> None:
        try:
            self.validate_license_plate(self.tx_search.get())
        except Exception as err:
            print(f"[-] {err}")
            messagebox.showerror("Matricula no valida", err)
            return

        aux = vehicle_class(license_plate=self.tx_search.get())
        vehicle = db_vehicle.search(self, aux)
        if vehicle is None:
            return
        
        self.enable_search()
        self.tx_license_plate.insert(0, vehicle.get_license_plate())
        self.tx_license_plate.configure(state=DISABLED)
        
        try:
            name = name_by_id("customer", vehicle.get_customer_id())
            self.opm_customer_name.set(name)
        except Exception as err:
            print(f"[-] {err}")
            messagebox.showerror("Error", "Error en la búsqueda")
        
        self.tx_model.insert(0, vehicle.get_model())
        self.tx_brand.insert(0, vehicle.get_brand())
        
    def new_vehicle(self) -> None:
        self.tx_license_plate.configure(state=ENABLE)
        self.opm_customer_name.configure(state=ENABLE)
        self.tx_model.configure(state=ENABLE)
        self.tx_brand.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_vehicle()
        self.band = True
        return
    
    def save_vehicle(self) -> None:            
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("save_vehicle_error", error)
            return
        
        try:
            license_plate = clean_str(self.tx_license_plate.get())
            model = clean_str(self.tx_model.get())
            brand = clean_str(self.tx_brand.get())
            
            vehicle = vehicle_class(license_plate, find_id(self.customers, self.opm_customer_name.get()), model, brand)
            
            # print(f"Matricula -> {vehicle.get_license_plate()}")
            # print(f"Customer ID -> {vehicle.get_customer_id()}")
            # print(f"Modelo -> {vehicle.get_model()}")
            # print(f"Marca -> {vehicle.get_brand()}")
            
            if self.band == True:
                db_vehicle.save(self, vehicle)
                messagebox.showinfo("Exitoso", "Vehiculo guardado exitosamente!")
            else:
                db_vehicle.edit(self, vehicle)
                messagebox.showinfo("Exitoso", "Vehiculo editado exitosamente!")
            self.default()
        except Exception as err:
            print(f"[-] save_vehicle: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} vehiculo en BD")
        finally:
            self.band = None
    
    def remove_vehicle(self) -> None:
        self.tx_license_plate.configure(state=ENABLE)
        
        try:
            aux = vehicle_class(license_plate=self.tx_license_plate.get())
            self.tx_license_plate.configure(state=DISABLED)
            db_vehicle.remove(self, aux)
            self.default()
            messagebox.showinfo("Exitoso", "Vehiculo eliminado exitosamente!")
        except Exception as err:
            print(f"[-] remove_vehicle: {err}")
            messagebox.showerror("Error", "No se logro eliminar el vehiculo")
        
    def edit_vehicle(self) -> None:
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_remove.configure(state=DISABLED)
        self.band = False
    
    def clear_vehicle(self):
        self.tx_license_plate.delete(0, END)
        self.opm_customer_name.configure(values=list(self.customers.values()))
        self.opm_customer_name.set(next(iter(self.customers.values())) if len(self.customers) > 0 else "No disponible")
        self.tx_brand.delete(0, END)
        self.tx_model.delete(0, END)
    
    def default(self):
        # Update list of customers
        self.customers = available_customers(self.profile.get_id())
        
        self.tx_license_plate.configure(state=ENABLE)
        self.opm_customer_name.configure(state=ENABLE)
        self.tx_model.configure(state=ENABLE)
        self.tx_brand.configure(state=ENABLE)
        self.clear_vehicle()
        
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_license_plate.configure(state=DISABLED)
        self.opm_customer_name.configure(state=DISABLED)
        self.tx_model.configure(state=DISABLED)
        self.tx_brand.configure(state=DISABLED)
    
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

        self.tx_license_plate.configure(state=ENABLE)
        self.opm_customer_name.configure(state=ENABLE)
        self.tx_model.configure(state=ENABLE)
        self.tx_brand.configure(state=ENABLE)
        self.clear_vehicle()

    def validate(self) -> None:
        entry_empty(self.tx_license_plate, "Matricula")
        entry_empty(self.opm_customer_name, "Cliente")
        entry_empty(self.tx_model, "Modelo")
        entry_empty(self.tx_brand, "Marca")

        if self.opm_customer_name.get() == "No disponible":
            raise Exception("No se encontraron clientes")

        if not is_alphabetic(self.tx_brand.get()):
            raise Exception("Marca no valido")

        if len(self.tx_model.get()) > 30:
            raise Exception("Tamaño maximo de modelo: 30 caracteres")

        if len(self.tx_brand.get()) > 20:
            raise Exception("Tamaño maximo de marca: 20 caracteres")
        
        self.validate_license_plate(self.tx_license_plate.get())
        
        # True = save, False = edit
        if self.band:
            if not license_plate_available(self.tx_license_plate.get(), "vehicle"):
                raise Exception("Matricula ya registrada")

    def validate_license_plate(self, license: str) -> None:
        if not (6 <= len(license) <= 7):
            raise Exception("La matricula debe contener 6 o 7 caracteres")