from tkinter import messagebox
import database as con
from customer import customer as customer_class
from db_functions import name_available, max_folio

table = "customer"

class db_customer:
    def save(self, customer: customer_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            name_available(customer.get_name(), table)
            self.sql = f"INSERT INTO {table}(id, name, user_id, phone) VALUES (%s,%s,%s,%s)"
            self.data = (
                customer.get_id(),
                customer.get_name(),
                customer.get_user_id(),
                customer.get_phone(),
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar cliente")
        finally:
            self.conn.close()
        
    def search(self, customer: customer_class) -> customer_class:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            aux = None
            self.sql = f"SELECT id, user_id, name, phone FROM {table} WHERE id={customer.get_id()}"
            self.cursor1.execute(self.sql)
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row[0] is not None:
                aux = customer_class(int(row[0]), int(row[1]), row[2], row[3])
        except:
            messagebox.showerror("Error", "No se encontro el cliente")
        return aux
    
    def edit(self, customer: customer_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s, user_id=%s, phone=%s WHERE id={customer.get_id()}"
            self.data = (
                customer.get_name(),
                customer.get_user_id(),
                customer.get_phone()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_customer: {err}")
            raise Exception(f"Error al editar cliente: {err}")
        finally:
            self.conn.close()

    def remove(self, customer: customer_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={customer.get_id()}"
            self.cursor1.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_customer: {err}")
            raise Exception(f"Error al eliminar cliente: {err}")
        finally:
            self.conn.close()

    def get_max_id(self) -> int:
        return max_folio(table)
    
    def close(self):
        self.conn.close()