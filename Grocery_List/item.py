class Item:
    def __init__(self,name,number,price):
        self.item_name = name
        self.item_number = number
        self.item_price = price
    
    def calculate_total_price(self):
        self.item_price = (self.item_number*self.item_price)

