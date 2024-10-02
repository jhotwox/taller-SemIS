class customer:
    def __init__(self, id: int = 0, user_id: int = 0, name: str = "", phone: str = ""):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.phone = phone
    
    def get_id(self):
        return self.id
    
    def get_user_id(self):
        return self.user_id
    
    def get_name(self):
        return self.name
    
    def get_phone(self):
        return self.phone