from tkinter import messagebox
import database as con
from repair import repair as repair_class
from db_functions import max_folio

table = "repair"

class db_repair:
    def save(self, repair: repair_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(folio, license_plate, date_in, date_out) VALUES (%s,%s,%s,%s)"
            self.data = (
                repair.get_folio(),
                repair.get_license_plate(),
                repair.get_date_in(),
                repair.get_date_out()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar reparación")
        finally:
            self.conn.close()
        
    def search(self, repair: repair_class) -> repair_class:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            aux = None
            self.sql = f"SELECT * FROM {table} WHERE folio={repair.get_folio()}"
            self.cursor1.execute(self.sql)
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row[0] is not None:
                aux = repair_class(int(row[0]), row[1], row[2], row[3])
        except:
            messagebox.showerror("Error", "No se encontro el folio")
        return aux    

    def edit(self, repair: repair_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"UPDATE {table} SET license_plate=%s, date_in=%s, date_out=%s WHERE id={repair.get_folio()}"
            self.data = (
                repair.get_license_plate(),
                repair.get_date_in(),
                repair.get_date_out()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_repair: {err}")
            raise Exception(f"Error al editar reparación: {err}")
        finally:
            self.conn.close()

    def remove(self, repair: repair_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE folio={repair.get_folio()}"
            self.cursor1.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_repair: {err}")
            raise Exception(f"Error al eliminar reparación: {err}")
        finally:
            self.conn.close()

    def get_max_folio(self) -> int:
        return max_folio(table)
    
    def close(self):
        self.conn.close()