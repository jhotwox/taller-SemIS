from customtkinter import CTk, CTkButton as Button, DISABLED
from user import user as user_class
# from login import Login
from users import Users
from customers import Customers
from vehicles import Vehicles
from parts import Parts
from repairs import Repairs

class Menu:
    def __init__(self, profile: user_class):
        self.window = CTk()
        self.window.title("Menu")
        self.window.config(width=400, height=400)
        
        self.btUsers = Button(self.window, text="Usuarios", command=self.openUsers)
        self.btUsers.grid(row=0, column=0, padx=10, pady=10)
        
        self.btCustomer = Button(self.window, text="Clientes", command=lambda: self.openCustomers(profile=profile))
        self.btCustomer.grid(row=0, column=1, padx=10, pady=10)
        
        self.btCars = Button(self.window, text="Vehiculos", command=lambda: self.openVehicles(profile=profile))
        self.btCars.grid(row=1, column=0, padx=10, pady=10)
        
        self.btRepairs = Button(self.window, text="Reparaciones", command=lambda: self.openRepairs(profile=profile))
        self.btRepairs.grid(row=1, column=1, padx=10, pady=10)
        
        self.btParts = Button(self.window, text="Partes", command=self.openParts)
        self.btParts.grid(row=2, column=0, padx=10, pady=10)
        
        self.btExit = Button(self.window, text="Salir", command=self.exit)
        self.btExit.grid(row=2, column=1, padx=10, pady=10)
        
        if profile.get_profile() == "secretaria":
            self.btUsers.configure(state=DISABLED)
            self.btRepairs.configure(state=DISABLED)
            self.btParts.configure(state=DISABLED)
        
        if profile.get_profile() == "mecanico":
            self.btUsers.configure(state=DISABLED)
            self.btCustomer.configure(state=DISABLED)
            self.btParts.configure(state=DISABLED)

        self.window.mainloop()
    
    def openUsers(self) -> None:
        self.window.destroy()
        Users()
    
    def openCustomers(self, profile: user_class) -> None:
        self.window.destroy()
        Customers(profile=profile)

    def openVehicles(self, profile: user_class) -> None:
        self.window.destroy()
        Vehicles(profile=profile)

    def openRepairs(self, profile: user_class) -> None:
        self.window.destroy()
        Repairs(profile=profile)

    def openParts(self) -> None:
        self.window.destroy()
        Parts()
        
    def exit(self) -> None:
        self.window.destroy()
        # Login()