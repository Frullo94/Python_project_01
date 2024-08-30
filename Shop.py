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

def help_command(self):
    """
    Prints the list of commands available for the user.
    """
    print("List of commands:")
    print("1. add")
    print("2. list")
    print("3. sell")
    print("4. profits")
    print("5. exit")
    print("6. help")
    
def save_data(self, filename="data.json"):
    """
    Saves the product data in a JSON file.
    """
    with open(filename, 'w') as f:
        data = {name: product.to_dict() for name, product in self.products.items()}
        json.dump(data, f)

def load_data(self, filename="data.json"):
    """
    Loads product data from a JSON file.
    """
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("{}")  # Create an empty JSON file

    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if not content:
                data = {}
            else:
                data = json.loads(content)
            self.products = {name: Product.from_dict(product_data) for name, product_data in data.items()}
    except FileNotFoundError:
        print("Warning, data.json not found")
        pass

def main():
    shop = Shop()
    shop.load_data()
    while True:
        try:
            command = input("Select a command (type -help- to see available commands) ")
            if command == "help":
                shop.help_command()
            elif command == "add":
                name = input("Product name: ").lower()
                
                while True:
                    quantity_str = input("Product quantity: ")
                    
                    if "." in quantity_str:
                        print("Error, quantity must be an integer, not a decimal")
                        continue
                    try:
                        quantity = int(quantity_str)
                        if quantity <= 0:
                            print("Error, quantity must be a positive integer")
                            continue
                        break
                    except ValueError:
                        print("Error, please enter a valid positive integer")
                        continue

                selling_price = float(input("Enter the selling price: "))
                purchase_price = float(input("Enter the purchase price: "))
                shop.add_product(name, quantity, selling_price, purchase_price)
            elif command == "list":
                shop.show_list()
            elif command == "sell":
                while True:
                    name = input("Enter the sold product: ").lower()
                    try:
                        quantity = int(input("Enter the quantity sold: "))
                        shop.record_sale(name, quantity)
                        print("Sale recorded")  # debug print
                        
                        another = input("Do you want to add another product? (yes/no): ").lower()
                        print(f"Response received: '{another}'")  # debug print
                        if another == "no":
                            break
                    except ValueError:
                        print("Error, please enter a valid integer")
            elif command == "profits":
                gross_profit, net_profit = shop.calculate_profit()
                print(f"Gross revenue: {gross_profit}, Net profit: {net_profit}")
            elif command == "exit":
                print("Goodbye")
                break
            else:
                print("Command not found")
            
            shop.save_data()

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
