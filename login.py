from customtkinter import CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk
from tkinter import messagebox
from functions import is_empty
from db_user import db_user
from user import user as user_class
from menu import Menu

class Login:
    def __init__(self):
        self.window = CTk()
        self.window.title("Login")
        self.window.config(width=400, height=400)

        self.lbTitle = Label(self.window, text="Login", font=("Calisto MT", 36, "bold"))
        self.lbTitle.grid(row=0, column=1, pady=20)

        # self.lbUsername = Label(self.window, text="Username", font=("Calisto MT", 16))
        # self.lbUsername.grid(row=1, column=0)
        self.txUsername = Entry(self.window, width=200, placeholder_text="Username")
        self.txUsername.grid(row=1, column=1, padx=20, pady=10)
        self.txUsername.insert(0, "cristian")
        
        # self.lbPass = Label(self.window, text="Contraseña", font=("Calisto MT", 16))
        # self.lbPass.grid(row=2, column=0, pady=10)
        self.txPass = Entry(self.window, width=200, placeholder_text="Contraseña", show="*")
        self.txPass.grid(row=2, column=1, padx=20, pady=10)
        self.txPass.insert(0, "unodostres")
        
        self.btLogin = Button(self.window, text="Ingresar", command=self.login)
        self.btLogin.grid(row=3, column=1, pady=15)
        
        self.window.mainloop()

    def validate(self) -> bool:
        username = self.txUsername.get()
        password = self.txPass.get()
        
        if is_empty(username):
            messagebox.showwarning("Campo vacio", "El campo username no debe de estar vacio")
            return False
        if is_empty(password):
            messagebox.showwarning("Campo vacio", "El campo contraseña no debe de estar vacio")
            return False
        if len(password) < 6:
            messagebox.showwarning("Invalido", "La contraseña es demasiado corta")
            return False
        return True

    def login(self):
        username = self.txUsername.get()
        password = self.txPass.get()
        
        if not self.validate():
            return
        
        aux = user_class(username=username, password=password)
        self.user = db_user.authenticate(self, aux)
        
        if self.user is not None:
            # messagebox.showinfo("Validado", "Usuario auntentificado")
            self.window.destroy()
            Menu(self.user)

Login()