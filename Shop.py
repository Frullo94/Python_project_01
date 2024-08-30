import json
import os

class Product:
    def __init__(self, name, quantity, selling_price, purchase_price):
        """
        Initialize a new Product object with name, quantity, selling price, purchase price.
        """
        self.name = name
        self.quantity = quantity
        self.selling_price = selling_price
        self.purchase_price = purchase_price
    
    def to_dict(self):
        """
        Converts the Product object into a dictionary.
        """
        return {
            "name": self.name,
            "quantity": self.quantity,
            "selling_price": self.selling_price,
            "purchase_price": self.purchase_price
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Product object from a dictionary.
        """
        return cls(data["name"], data["quantity"], data["selling_price"], data["purchase_price"])

class Shop:
    def __init__(self):
        """
        Initialize a new Shop object with no products.
        """
        self.products = {}

    def add_product(self, name, quantity, selling_price, purchase_price):
        """
        Adds a product to the store or updates the quantity if the product already exists.
        """
        if name in self.products:
            self.products[name].quantity += quantity
        else:
            self.products[name] = Product(name, quantity, selling_price, purchase_price)

    def show_list(self):
        """
        Shows the list of products.
        """
        for product in self.products.values():
            print(f"Name: {product.name}, Quantity: {product.quantity}, Selling Price: {product.selling_price}, Purchase Price: {product.purchase_price}")

    def record_sale(self, name, quantity):
        """
        Records a sale of a product, decreasing the available quantity.
        """
        if name in self.products and self.products[name].quantity >= quantity:
            self.products[name].quantity -= quantity
        else:
            raise Exception("Quantity exceeds availability")

    def calculate_profit(self):
        """
        Calculates the total revenue, costs, and then the profit.
        """
        gross_profit = sum(product.selling_price * product.quantity for product in self.products.values())
        total_costs = sum(product.purchase_price * product.quantity for product in self.products.values())
        net_profit = gross_profit - total_costs
        return gross_profit, net_profit
