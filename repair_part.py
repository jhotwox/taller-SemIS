class repair_part:
    def __init__(self, folio: int = 0, part_id: int = 0, quantity: int = 0, fault: str= ""):
        self.folio = folio
        self.part_id = part_id
        self.quantity = quantity
        self.fault = fault

    def get_folio(self):
        return self.folio
    
    def get_part_id(self):
        return self.part_id
    
    def get_quantity(self):
        return self.quantity

    def get_fault(self):
        return self.fault
