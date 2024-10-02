from tkinter import messagebox
import database as con
from part import part as part_class
from db_functions import max_folio 

table = "part"

class db_part:
    
    def save(self, part: part_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            
            self.sql = f"INSERT INTO {table}(id, description, stock) VALUES (%s,%s,%s)"
            self.data = (
                part.get_id(),
                part.get_description(),
                part.get_stock(),
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            raise err
        finally:
            self.conn.close()
        
    def search(self, part: part_class) -> part_class:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE id={part.get_id()}"
            self.cursor1.execute(self.sql)
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row[0] is not None:
                return part_class(int(row[0]), row[1], row[2])
            return None
        except:
            messagebox.showerror("Error", "No se encontro la parte")
    
    def edit(self, part: part_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"UPDATE {table} SET description=%s, stock=%s WHERE id={part.get_id()}"
            self.data = (
                part.get_description(),
                part.get_stock()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_part: {err}")
            raise Exception(f"Error al editar parte: {err}")
        finally:
            self.conn.close()
            
    def remove(self, part: part_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={part.get_id()}"
            self.cursor1.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_part: {err}")
            raise Exception(f"Error al eliminar pieza: {err}")
        finally:
            self.conn.close()

    def get_max_id(self) -> int:
        return max_folio(table)
    
    def close(self):
        self.conn.close()
        
# try:
    # print(db_vehicle.search(None, vehicle_class(license_plate="AAA111")))
# except Exception as err:
    # print(f"[-] Err: {err}")
