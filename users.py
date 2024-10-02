from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar
from tkinter import messagebox
from functions import entry_empty
from db_user import db_user
from user import user as user_class

class Users:
    def __init__(self):
        self.band = None
        self.window = CTk()
        self.window.title("Usuarios")
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
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_user)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        
        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0)
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0)
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_username = Label(fr_entry, text="Username")
        self.lb_username.grid(row=2, column=0, pady=0)
        self.tx_username = Entry(fr_entry, placeholder_text="Username")
        self.tx_username.grid(row=2, column=1, pady=5)

        self.lb_password = Label(fr_entry, text="Contraseña")
        self.lb_password.grid(row=3, column=0, pady=0)
        self.tx_password = Entry(fr_entry, placeholder_text="Contraseña")
        self.tx_password.grid(row=3, column=1, pady=5, padx=20)
        self.lb_profile = Label(fr_entry, text="Perfil")
        self.lb_profile.grid(row=4, column=0, pady=0)
        self.selected_profile = StringVar(value="admin")
        self.opm_profile = OptMenu(fr_entry, values=(["admin", "secretaria", "mecanico"]), variable=self.selected_profile)
        self.opm_profile.grid(row=4, column=1, pady=5)
        
        
        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_user)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_user)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_user)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_user)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        
        self.default()
        
        self.window.mainloop()
    
    def search_user(self) -> None:
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning("Error", "Ingrese un ID válido")
            return
        
        aux = user_class(id=int(self.tx_search.get()))
        user = db_user.search(self, aux)
        if user is None:
            return
        
        self.enable_search()
        self.tx_id.insert(0, user.id)
        self.tx_id.configure(state=DISABLED)
        self.tx_name.insert(0, user.name)
        self.tx_username.insert(0, user.username)
        self.tx_password.insert(0, user.password)
        self.opm_profile.set(user.profile)
    
    def remove_user(self) -> None:
        self.tx_id.configure(state=ENABLE)
        if not self.tx_id.get().isdecimal():
            messagebox.showwarning("Error", "ID inválido")
            return
        
        try:
            aux = user_class(id=int(self.tx_id.get()))
            self.tx_id.configure(state=DISABLED)
            db_user.remove(self, aux)
            self.default()
            messagebox.showinfo("Exitoso", "Usuario eliminado exitosamente!")
        except Exception as err:
            print(f"[-] remove_user: {err}")
            messagebox.showerror("Error", "No se logro eliminar el usuario")
            
    def new_user(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_username.configure(state=ENABLE)
        self.tx_password.configure(state=ENABLE)
        self.opm_profile.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        
        self.clear_user()
        self.tx_id.insert(0, db_user.get_max_id(self)+1)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
    
    def save_user(self) -> None:
        try:
            entry_empty(self.tx_id, "ID")
            entry_empty(self.tx_name, "Nombre")
            entry_empty(self.tx_username, "Username")
            entry_empty(self.tx_password, "Contraseña")
            entry_empty(self.opm_profile, "Perfil")
        except Exception as error:
            messagebox.showwarning("Campo vacio", error)
            return
        
        if len(self.tx_password.get()) < 6:
            messagebox.showwarning("Contraseña demasiado corta", "La contraseña debe tener al menos 6 caracteres")
            return
        
        try:
            user = user_class(int(self.tx_id.get()),self.tx_name.get(), self.tx_username.get(), self.tx_password.get(), self.opm_profile.get())
            if self.band == True:
                db_user.save(self, user)
                messagebox.showinfo("Exitoso", "Usuario guardado exitosamente!")
            else:
                db_user.edit(self, user)
                messagebox.showinfo("Exitoso", "Usuario editado exitosamente!")
            self.default()
        except Exception as err:
            print(f"[-] saveUser: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} usuario en BD")
        finally:
            self.band = None
        
    def edit_user(self) -> None:
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.band = False
    
    def clear_user(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_username.delete(0, END)
        self.tx_password.delete(0, END)
        self.opm_profile.set("admin")
    
    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.clear_user()
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_username.configure(state=DISABLED)
        self.tx_password.configure(state=DISABLED)
        self.opm_profile.configure(state=DISABLED)
    
    def enable_search(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=ENABLE)
        self.bt_remove.configure(state=ENABLE)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_username.configure(state=ENABLE)
        self.tx_password.configure(state=ENABLE)
        self.opm_profile.configure(state=ENABLE)
        self.clear_user()