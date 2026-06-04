from fastapi import FastAPI
from models import Products
from db_conn import session,engine
import database_models  

app = FastAPI()


@app.get("/")
def greet():
    return {"message":"Hello Sorcerer supreme"}


data ={
    "firstname":"Sorcerrer",
    "lastname":"Supereme"
}
def introduce(firstname,lastname):
    print(f"my name is {firstname}-{lastname}")

#want to check just uncomment this 
# Unpacking the key value pairs
# introduce(**data)

products= [
    Products(id=1,name="phone",description="An iphone",price=99,quantity=10),
    Products(id=4,name="keyboard",description="An keyboard",price=99,quantity=10),
    Products(id=8,name="mouse",description="A mouse",price=99,quantity=10),
    Products(id=6,name="bag",description="A bag",price=99,quantity=10)
]

#Look all the models which inherits from the base class and register its schema with its metadata and create table in the database using the (engine)  connection string of the database (create_all)
database_models.Base.metadata.create_all(bind=engine)

def init_db():
    db=session()
    for product in products:
        # print(product.model_dump())
        db.add(database_models.Product(**product.model_dump()))
        
init_db()

@app.get("/products")
def getallproducts():
    #database connection 
    db = session()
    db.query()
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


    
@app.delete("/product/{id}")
def remove_product(id:int):
    for i in range(len(products)):
      if products[i].id == id:
        del products[i]
        return {"removed the product"}
        
    return "product is not found"

@app.put("/product")
def update_product(id:int , product:Products):
    for i in range(len(products)):
            if products[i].id == id:
                products[i] = product 
                return {"updated product":product}
    return {"product not found"}