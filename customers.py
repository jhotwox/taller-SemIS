from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, DISABLED, NORMAL as ENABLE, CTkFrame as Frame
from tkinter import messagebox
from functions import entry_empty, is_alphabetic, clean_str
from db_functions import available_customers, name_by_id, name_available
from customer import customer as customer_class
from db_customer import db_customer
from user import user as user_class

class Customers:
    def __init__(self, profile: user_class):
        self.profile = profile
        self.band = None
        self.window = CTk()
        self.window.title("Clientes")
        self.window.config(width=400, height=400)
        
        fr_search = Frame(self.window)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_entry = Frame(self.window)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        fr_button = Frame(self.window)
        fr_button.grid(row=2, column=0, sticky="nsw", padx=10, pady=10)
        
        self.lb_search = Label(fr_search, text="ID a buscar: ", font=("Calisto MT", 12))
        self.lb_search.grid(row=0, column=0, padx=5)
        self.tx_search = Entry(fr_search, placeholder_text="ID a buscar", width=200)
        self.tx_search.grid(row=0, column=1,  padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_customer)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        
        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0)
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        
        self.lb_user_name = Label(fr_entry, text="Usuario")
        self.lb_user_name.grid(row=1, column=0, pady=0)
        self.tx_user_name = Entry(fr_entry, fg_color="#222", border_color="#222")
        self.tx_user_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_user_id = Label(fr_entry, text="ID")
        self.lb_user_id.grid(row=1, column=2, pady=0)
        self.tx_user_id = Entry(fr_entry, width=72, fg_color="#222", border_color="#222")
        self.tx_user_id.grid(row=1, column=3, pady=5, padx=20)
        self.tx_user_name.insert(0, profile.get_name())
        self.tx_user_id.insert(0, profile.get_id())
        self.tx_user_name.configure(state=DISABLED)
        self.tx_user_id.configure(state=DISABLED)
        
        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=2, column=0, pady=0)
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=2, column=1, pady=5, padx=20)

        self.lb_phone = Label(fr_entry, text="Teléfono")
        self.lb_phone.grid(row=3, column=0, pady=0)
        self.tx_phone = Entry(fr_entry, placeholder_text="Teléfono")
        self.tx_phone.grid(row=3, column=1, pady=5, padx=20)

        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_customer)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_customer)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_customer)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_customer)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        
        self.default()
        
        self.window.mainloop()
    
    def search_customer(self) -> None:
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning("Error", "Ingrese un ID válido")
            return
        
        aux = customer_class(id=int(self.tx_search.get()))
        customer = db_customer.search(self, aux)
        if customer is None:
            return
        
        self.enable_search()
        self.tx_id.insert(0, customer.get_id())
        self.tx_id.configure(state=DISABLED)
        self.tx_user_id.insert(0, customer.get_user_id())
        self.tx_user_id.configure(state=DISABLED)
        
        try:
            name = name_by_id("user", customer.get_user_id())
        except Exception as err:
            print(f"[-] {err}")
            messagebox.showerror("Error", "Error en la búsqueda")
        self.tx_user_name.insert(0, name)
        self.tx_user_name.configure(state=DISABLED)
        
        self.tx_name.insert(0, customer.get_name())
        self.tx_phone.insert(0, customer.get_phone())
        
    def new_customer(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_phone.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_customer()
        self.tx_id.insert(0, db_customer.get_max_id(self)+1)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
    
    def save_customer(self) -> None:            
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("Error", error)
            return
        
        try:
            # print(f"ID -> {int(self.tx_id.get())}\nName -> {self.tx_name.get()}\n Phone -> {self.tx_phone.get()}")
            name = clean_str(self.tx_name.get())
            phone = clean_str(self.tx_phone.get())

            if self.band == True:
                customer = customer_class(int(self.tx_id.get()), self.profile.get_id(), name, phone)
                db_customer.save(self, customer)
                messagebox.showinfo("Exitoso", "Cliente guardado exitosamente!")
            else:
                self.tx_user_id.configure(state=ENABLE)
                customer = customer_class(int(self.tx_id.get()), self.tx_user_id.get(), name, phone)
                self.tx_user_id.configure(state=DISABLED)
                db_customer.edit(self, customer)
                messagebox.showinfo("Exitoso", "Cliente editado exitosamente!")
            self.default()
        except Exception as err:
            print(f"[-] save_customer: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} cliente en BD")
        finally:
            self.band = None
    
    def remove_customer(self) -> None:
        self.tx_id.configure(state=ENABLE)
        if not self.tx_id.get().isdecimal():
            messagebox.showwarning("Error", "ID inválido")
            return
        
        try:
            aux = customer_class(id=int(self.tx_id.get()))
            self.tx_id.configure(state=DISABLED)
            db_customer.remove(self, aux)
            self.default()
            messagebox.showinfo("Exitoso", "Cliente eliminado exitosamente!")
        except Exception as err:
            print(f"[-] remove_user: {err}")
            messagebox.showerror("Error", "No se logro eliminar el cliente")
        
    def edit_customer(self) -> None:
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_remove.configure(state=DISABLED)
        self.band = False
    
    def clear_customer(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_phone.delete(0, END)
        self.tx_user_name.delete(0, END)
        self.tx_user_id.delete(0, END)
    
    def default(self):
        # Update list of customers
        self.users = available_customers()
        
        self.tx_id.configure(state=ENABLE)
        self.tx_user_name.configure(state=ENABLE)
        self.tx_user_id.configure(state=ENABLE)
        self.clear_customer()
        
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        
        self.tx_user_name.insert(0, self.profile.get_name())
        self.tx_user_id.insert(0, self.profile.get_id())
        self.tx_id.configure(state=DISABLED)
        self.tx_user_name.configure(state=DISABLED)
        self.tx_user_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_phone.configure(state=DISABLED)
    
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

        self.tx_id.configure(state=ENABLE)
        self.tx_user_name.configure(state=ENABLE)
        self.tx_user_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_phone.configure(state=ENABLE)
        self.clear_customer()
        
    def validate(self) -> None:
        entry_empty(self.tx_id, "ID")
        entry_empty(self.tx_user_name, "Nombre usuario")
        entry_empty(self.tx_user_id, "ID usuario")
        entry_empty(self.tx_name, "Nombre")
        entry_empty(self.tx_phone, "Teléfono")

        if not is_alphabetic(self.tx_name.get()):
            raise Exception("Nombre no valido")

        if not self.tx_phone.get().isdecimal():
            raise Exception("Teléfono no valido")

        if len(self.tx_name.get()) > 20:
            raise Exception("Tamaño maximo de nombre: 20 caracteres")

        if len(self.tx_phone.get()) != 10:
            raise Exception("Campo Teléfono debe contener 10 caracteres")
        
        if not name_available(self.tx_name.get(), "customer"):
            raise Exception("Nombre ya registrado")
        