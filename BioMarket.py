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
            print(f"Nome: {product.name}, Quantità: {product.quantity}, Prezzo di vendita: {product.selling_price}, Prezzo di acquisto: {product.purchase_price}")

    def record_sale(self, name, quantity):
        """
        Records a sale of a product, decreasing the available quantity.
        
        """
        if name in self.products and self.products[name].quantity >= quantity:
            self.products[name].quantity -= quantity
        else:
            raise Exception("Quantità maggiore della disponibilità")
        # if name in self.products and self.products[name].quantity >= quantity:
        #     self.products[name].quantity -= quantity
        
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
        print("Lista dei comandi:")
        print("1. aggiungi")
        print("2. elenca")
        print("3. vendita")
        print("4. profitti")
        print("5. chiudi")
        print("6. aiuto")
    
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
                f.write("{}")  # Crea un file JSON vuoto

        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
                if not content:
                    data = {}
                else:
                    data = json.loads(content)
                self.products = {name: Product.from_dict(product_data) for name, product_data in data.items()}
        except FileNotFoundError:
            print("Attenzione, data.jason non trovato")
            pass

def main():
    shop = Shop()
    shop.load_data()
    while True:
        try:
            command = input("seleziona un comando (digitare -aiuto- per vedere i comandi disponibili) ")
            if command == "aiuto":
                    shop.help_command()
            elif command == "aggiungi":
                name = input("name prodotto: ").lower()
                
                while True:
                    quantity_str = input("quantità del prodotto: ")
                    
                    if "." in quantity_str:
                        print("Errore, la quantità deve essere un intero, non un decimale")
                        continue
                    try:
                        quantity = int(quantity_str)
                        if quantity <= 0:
                            print("Errore, la quantità deve essere intero positivo")
                            continue
                        break
                    except ValueError:
                            print("Errore, prego inserire un numero valido, intero positivo")
                            continue

                selling_price = float(input("Scrivere il prezzo di vendita: "))
                purchase_price = float(input("Scrivere il prezzo di acquisto: "))
                shop.add_product(name, quantity, selling_price, purchase_price)
            elif command == "elenca":
                    shop.show_list()
            elif command == "vendita":
                while True:
                    name = input("Scrivere il prodotto venduto: ").lower()
                    try:
                        quantity = int(input("Scrivere la quantità venduta: "))
                        shop.record_sale(name, quantity)
                        print("vendita registrata") # stampa di debug
                    
                        another = input("Vuoi aggiungere un altro prodotto? (si/no): ").lower()
                        print(f"Risposta ricevuta: '{another}'") # stampa di debug
                        if another == "no":
                            break
                    except ValueError:
                        print("Errore, prego inserire un numero intero valido")
            elif command == "profitti":
                    gross_profit, net_profit = shop.calculate_profit()
                    print(f"Incasso: {gross_profit}, Profitto netto: {net_profit}")
            elif command == "chiudi":
                    print("ciao")
                    break
            else:
                    print("comando non trovato")
                
            shop.save_data()

        except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()


