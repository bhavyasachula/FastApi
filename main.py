from fastapi import FastAPI
from models import Products
app = FastAPI()


@app.get("/")
def greet():
    return {"message":"Hello Sorcerer supreme"}

products= [
    Products(id=1,name="phone",description="An iphone",price=99,quantity=10),
    Products(id=4,name="keyboard",description="An keyboard",price=99,quantity=10),
    Products(id=8,name="mouse",description="A mouse",price=99,quantity=10),
    Products(id=6,name="bag",description="A bag",price=99,quantity=10)
]
@app.get("/products")
def getallproducts():
    return products

@app.get("/product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id == id:
            return product
      
    return {"message":"product not found"}

@app.post("/product")
def add_product(product:Products):
    products.append(product)


    
@app.delete("/delete/{id}")
def remove_product(id:int):
    for i in range(products):
      if products[i].id == id:
        del products[i]
        return {"removed_product"}
        
    return "product is not found"

@app.put("/product")
def update_product(id:int , product:Products):
    for i in range(len(products)):
            if products[i].id == id:
                products[i] = product 
                return {"updated product":product}
    return {"product not found"}