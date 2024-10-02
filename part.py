class part:
    def __init__(self, id: int = 0, description: str = "", stock: int = 0):
        self.id = id
        self.description = description
        self.stock = stock
    
    def get_id(self):
        return self.id
    
    def get_description(self):
        return self.description
    
    def get_stock(self):
        return self.stock