import json
import os

class Product:
    def __init__(self, name, quantity, selling_price, purchase_price):
        """
        Inizializza un nuovo oggetto Product con nome, quantità, prezzo di vendita, prezzo di acquisto.

        """
        self.name = name
        self.quantity = quantity
        self.selling_price = selling_price
        self.purchase_price = purchase_price
    
    def to_dict(self):
        """
        Converte l'oggetto Product in un dizionario.
        
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
        Crea un oggetto Product da un dizionario.
        
        """
        return cls(data["name"], data["quantity"], data["selling_price"], data["purchase_price"])

class Shop:
    def __init__(self):
        """
        Inizializza un nuovo oggetto Shop senza prodotti.

        """
        self.products = {}

    def add_product(self, name, quantity, selling_price, purchase_price):
        """
        Aggiunge un prodotto al negozio o aggiorna la quantità se il prodotto esiste già.
        
        """
        if name in self.products:
            self.products[name].quantity += quantity
        else:
            self.products[name] = Product(name, quantity, selling_price, purchase_price)

    def show_list(self):
        """
        Mostra l'elenco dei prodotti.
        
        """
        for product in self.products.values():
            print(f"Nome: {product.name}, Quantità: {product.quantity}, Prezzo di vendita: {product.selling_price}, Prezzo di acquisto: {product.purchase_price}")

    def record_sale(self, name, quantity):
        """
        Registra una vendita di un prodotto, diminuendo la quantità disponibile.
        
        """
        if name in self.products and self.products[name].quantity >= quantity:
            self.products[name].quantity -= quantity
        else:
            raise Exception("Quantità maggiore della disponibilità")
        # if name in self.products and self.products[name].quantity >= quantity:
        #     self.products[name].quantity -= quantity
        
    def calculate_profit(self):
        """
        Calcola il totale delle entrate, dei costi e poi il profitto.
        
        """
        gross_profit = sum(product.selling_price * product.quantity for product in self.products.values())
        total_costs = sum(product.purchase_price * product.quantity for product in self.products.values())
        net_profit = gross_profit - total_costs
        return gross_profit, net_profit
    
    def help_command(self):
        """
        Stampa l'elenco dei comandi disponibili per l'utente.
        
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
        Salva i dati dei prodotti in un file JSON.

        """
        with open(filename, 'w') as f:
            data = {name: product.to_dict() for name, product in self.products.items()}
            json.dump(data, f)
