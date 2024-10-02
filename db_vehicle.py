from tkinter import messagebox
import database as con
from vehicle import vehicle as vehicle_class
from db_functions import license_plate_available

table = "vehicle"

class db_vehicle:
    
    def save(self, vehicle: vehicle_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            
            license_plate_available(vehicle.get_license_plate(), table)
            self.sql = f"INSERT INTO {table}(license_plate, customer_id, model, brand) VALUES (%s,%s,%s,%s)"
            self.data = (
                vehicle.get_license_plate(),
                vehicle.get_customer_id(),
                vehicle.get_model(),
                vehicle.get_brand()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            raise err
        finally:
            self.conn.close()
        
    def search(self, vehicle: vehicle_class) -> vehicle_class:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE license_plate='{vehicle.get_license_plate()}'"
            self.cursor1.execute(self.sql)
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row[0] is not None:
                return vehicle_class(row[0], int(row[1]), row[2], row[3])
            return None
        except:
            messagebox.showerror("Error", "No se encontro el vehiculo")
    
    def edit(self, vehicle: vehicle_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"UPDATE {table} SET customer_id=%s, model=%s, brand=%s WHERE license_plate='{vehicle.get_license_plate()}'"
            self.data = (
                vehicle.get_customer_id(),
                vehicle.get_model(),
                vehicle.get_brand()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_vehicle: {err}")
            raise Exception(f"Error al editar vehiculo: {err}")
        finally:
            self.conn.close()
            
    def remove(self, vehicle: vehicle_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE license_plate='{vehicle.get_license_plate()}'"
            self.cursor1.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_vehicle: {err}")
            raise Exception(f"Error al eliminar vehiculo: {err}")
        finally:
            self.conn.close()

    def close(self):
        self.conn.close()
        
        
# try:
#     print(db_vehicle.search(None, vehicle_class(license_plate="AAA111")))
# except Exception as err:
#     print(f"[-] Err: {err}")