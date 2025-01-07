import os
import json

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }
        
class InventorySystem:
    def __init__(self, file_name):
        self.file_name = file_name
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w') as file:
                json.dump([], file)
                
    def add_product(self, product):
        try:
            products = self._read_products()
            if any(p['name'] == product.name for p in products):
                print(f"Product with name '{product.name}' already exists.")
                return
            
            products.append(product.to_dict())
            self._write_products(products)
            print(f"Product '{product.name}' added successfully.")
            
        except Exception as e:
            print(f"Error adding product.{e}")
            
    def list_products(self):
        try:
            products = self._read_products()
            if not products:
                print("No products in inventory.")
                return
            
            sorted_products = sorted(products, key=lambda p: p['name'].lower())
            print("Inventory:")
            for i, product in enumerate(sorted_products, start=1):
                print(f"{i}. Name: {product['name']}, Price: Rs. {product['price']}, Quantity: {product['quantity']}")
                
        except Exception as e:
            print(f"Error listing products: {e}")
        
    def delete_product(self, product_name):
        try:
            products = self._read_products()
            updated_products = [product for product in products if product['name'] != product_name]
            
            if len(products) == len(updated_products):
                print(f"Product '{product_name}' not found.")
                return
            self._write_products(updated_products)
            print(f"Product '{product_name}' deleted successfully.")
            
        except Exception as e:
            print(f"Error deleting product.{e}")
    def _read_products(self):
        with open(self.file_name, 'r') as file:
            return json.load(file)
        
    def _write_products(self, products):
        with open(self.file_name, 'w') as file:
            json.dump(products, file, indent=4)
            
#Main
if __name__ == "__main__":
    inventory = InventorySystem("inventory.json")
    print("Inventory Management System")
    
    while True:
        print("1. Add product")
        print("2. List product")
        print("3. Delete product")
        print("4. Exit")
        
        try:
            option = int(input("Choose an option:"))
                
            if option == 1:
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                product = Product(name, price, quantity)
                inventory.add_product(product)
            elif option == 2:
                inventory.list_products()
            elif option == 3:
                name = input("Enter the name of the product to delete: ")
                inventory.delete_product(name)
            elif option == 4:
                print("Program end.")
                break
            else:
                print("Invalid option.")
            
        except ValueError:
            print("Invalid input. Please enter valid data.")
        except Exception as e:
            print(f"Invalid. {e}")