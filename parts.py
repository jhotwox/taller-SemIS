from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, DISABLED, NORMAL as ENABLE, CTkFrame as Frame
from tkinter import messagebox
from functions import entry_empty, clean_str
from part import part as part_class
from db_part import db_part

from user import user as user_class

class Parts:
    def __init__(self):
        self.band = None
        self.window = CTk()
        self.window.title("Piezas")
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
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_part)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        
        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0)
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_description = Label(fr_entry, text="Descripción")
        self.lb_description.grid(row=1, column=0, pady=0)
        self.tx_description = Entry(fr_entry, placeholder_text="Descripción")
        self.tx_description.grid(row=1, column=1, pady=5, padx=20)
        
        self.lb_stock = Label(fr_entry, text="Stock")
        self.lb_stock.grid(row=2, column=0, pady=0)
        self.tx_stock = Entry(fr_entry, placeholder_text="Stock")
        self.tx_stock.grid(row=2, column=1, pady=5, padx=20)


        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_part)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_part)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_part)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_part)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        
        self.default()
        
        self.window.mainloop()
    
    def search_part(self) -> None:
        
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning("Error", "Ingrese un ID válido")
            return
        
        aux = part_class(id=int(self.tx_search.get()))
        part = db_part.search(self, aux)
        if part is None:
            return
        
        self.enable_search()
        self.tx_id.insert(0, part.get_id())
        self.tx_id.configure(state=DISABLED)
        self.tx_description.insert(0, part.get_description())
        self.tx_stock.insert(0, part.get_stock())
        
    def new_part(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_description.configure(state=ENABLE)
        self.tx_stock.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_part()
        self.tx_id.insert(0, str(db_part.get_max_id(self)+1))
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
    
    def save_part(self) -> None:            
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("save_part_error", error)
            return
        
        try:
            description = clean_str(self.tx_description.get())
            stock = clean_str(self.tx_stock.get())
            
            part = part_class(int(self.tx_id.get()), description, stock)
            
            # print(f"Matricula -> {part.get_license_plate()}")
            # print(f"Modelo -> {part.get_model()}")
            # print(f"Marca -> {part.get_brand()}")
            
            if self.band == True:
                db_part.save(self, part)
                messagebox.showinfo("Exitoso", "Pieza guardado exitosamente!")
            else:
                db_part.edit(self, part)
                messagebox.showinfo("Exitoso", "Pieza editado exitosamente!")
            self.default()
        except Exception as err:
            print(f"[-] save_part: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} pieza en BD")
        finally:
            self.band = None
    
    def remove_part(self) -> None:
        self.tx_id.configure(state=ENABLE)
        if not self.tx_id.get().isdecimal():
            messagebox.showwarning("Error", "ID inválido")
            return
        
        try:
            aux = part_class(id=int(self.tx_id.get()))
            self.tx_id.configure(state=DISABLED)
            db_part.remove(self, aux)
            self.default()
            messagebox.showinfo("Exitoso", "Pieza eliminado exitosamente!")
        except Exception as err:
            print(f"[-] remove_part: {err}")
            messagebox.showerror("Error", "No se logro eliminar la pieza")
        return
        
    def edit_part(self) -> None:
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_remove.configure(state=DISABLED)
        self.band = False
    
    def clear_part(self):
        self.tx_id.delete(0, END)
        self.tx_description.delete(0, END)
        self.tx_stock.delete(0, END)
    
    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.tx_description.configure(state=ENABLE)
        self.tx_stock.configure(state=ENABLE)
        self.clear_part()
        
        self.bt_edit.configure(state=DISABLED)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_description.configure(state=DISABLED)
        self.tx_stock.configure(state=DISABLED)
    
    def enable_search(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=ENABLE)
        self.bt_remove.configure(state=ENABLE)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_description.configure(state=ENABLE)
        self.tx_stock.configure(state=ENABLE)
        self.clear_part()

    def validate(self) -> None:
        entry_empty(self.tx_id, "ID")
        entry_empty(self.tx_description, "Descripción")
        entry_empty(self.tx_stock, "Stock")
        
        if len(self.tx_description.get()) > 50:
            raise Exception("Tamaño maximo de descripción: 50 caracteres")

        if len(self.tx_stock.get()) > 10:
            raise Exception("Tamaño maximo de stock: 10 caracteres")
        
        if not self.tx_stock.get().isdecimal():
            raise Exception("Ingresa un stock válido")