from tkinter import messagebox
import database as con
# from repair import repair as repair_class
from repair_part import repair_part as repair_part_class

table = "repair_part"

class db_repair_part:
    def save(self, repair_part: repair_part_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(folio, part_id, quantity, fault) VALUES (%s,%s,%s,%s)"
            self.data = (
                repair_part.get_folio(),
                repair_part.get_part_id(),
                repair_part.get_quantity(),
                repair_part.get_fault()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error db_repair_part save", "Error al guardar reparación_parte")
        finally:
            self.conn.close()
        
    def search(self, repair_part: repair_part_class) -> repair_part_class:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            aux = None
            self.sql = f"SELECT * FROM {table} WHERE folio={repair_part.get_folio()} AND part_id={repair_part.get_part_id()}"
            self.cursor1.execute(self.sql)
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row[0] is not None:
                aux = repair_part_class(int(row[0]), int(row[1]), int(row[2]), row[3])
        except Exception as err:
            print(f"[-] search in db_repair_part: {err}")
            raise Exception(f"No se encontro el folio - parte")
        return aux

    def search_bool(self, repair_part: repair_part_class) -> bool:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            print("*-*-*-*-*-*-*-*-*-*-*")
            print("db_repair_part")
            print(f"search_bool\nFolio -> {repair_part.get_folio()}\nPart_id -> {repair_part.get_part_id()}")
            print("*-*-*-*-*-*-*-*-*-*-*")
            self.sql = f"SELECT COUNT(*) FROM {table} WHERE folio={repair_part.get_folio()} AND part_id={repair_part.get_part_id()}"
            self.cursor1.execute(self.sql)
            row = self.cursor1.fetchone()
            self.conn.commit()
            return row[0]
        except Exception as err:
            print(f"[-] search in db_repair_part: {err}")
            raise Exception(f"No se encontro el folio - parte")
        finally:
            self.conn.close()

    def edit(self, repair_part: repair_part_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"UPDATE {table} SET quantity=%s, fault=%s WHERE id={repair_part.get_folio()} AND part_id={repair_part.get_part_id()}"
            self.data = (
                repair_part.get_quantity(),
                repair_part.get_fault()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_repair_part: {err}")
            raise Exception(f"Error al editar reparación_parte: {err}")
        finally:
            self.conn.close()

    def remove(self, repair_part: repair_part_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE folio={repair_part.get_folio()} and part_id={repair_part.get_part_id()}"
            self.cursor1.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_repair_part: {err}")
            raise Exception(f"Error al eliminar reparación_parte: {err}")
        finally:
            self.conn.close()
    
    def close(self):
        self.conn.close()