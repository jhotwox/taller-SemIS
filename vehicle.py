class vehicle:
    def __init__(self, license_plate: str = "", customer_id: int = 0, model: str = "", brand: str = ""):
        self.license_plate = license_plate
        self.customer_id = customer_id
        self.model = model
        self.brand = brand
    
    def get_license_plate(self):
        return self.license_plate
    
    def get_customer_id(self):
        return self.customer_id
    
    def get_model(self):
        return self.model
    
    def get_brand(self):
        return self.brand