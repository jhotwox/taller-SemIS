class repair:
    def __init__(self, folio: int = 0, license_plate: str = "", date_in: str = "", date_out: str = ""):
        self.folio = folio
        self.license_plate = license_plate
        self.date_in = date_in
        self.date_out = date_out
    
    def get_folio(self):
        return self.folio
    
    def get_license_plate(self):
        return self.license_plate
    
    def get_date_in(self):
        return self.date_in
    
    def get_date_out(self):
        return self.date_out