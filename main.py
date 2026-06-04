from fastapi import Depends,FastAPI
from models import Products
from db_conn import session,engine
import database_models  
from sqlalchemy.orm import Session

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

def get_db():
    db = session()
    try:
       yield db
       #Internally fast api does this init_db(db) is passes the db object and after the execution is completed it comes here and execute the finally and close the connection of db
    finally:
        db.close()


def init_db():
    db=session()
    count = db.query(database_models.Product).count()
    
    if count==0:
        for product in products:
        # print(product.model_dump())
        # class Products(BaseModel):
        # id:int
        # name:str
        # description:str
        # price:float
        # quantity:int
        # wht we are doing is import the Product object from the databse_models.Products(id=,name=,description,price=,quantity=)  so by doing the **product.model_dump()  so internally it becomes this "Products(id=,name=,description,price=,quantity=)" and by unpacking we are adding the data like this "Products(id=1,name=iphone,description=an iphone mobile,price=10,quantity=10)"
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
        db.close()

init_db()

@app.get("/products")
def getallproducts(db:Session = Depends(get_db)):

#     What does .all() do?
   # db.query(Product).all()
 # means:
# Give me every row from the Product table.
# SQLAlchemy generates SQL similar to:
# SELECT *
# FROM product;
# and sends it to the database.
    # means db.query(database_models.Product) wht it means is that query the product table in the databse but in python we have mention the database_model.Product
    database_products = db.query(database_models.Product).order_by(database_models.Product.id).all()
    return database_products

@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session= Depends(get_db)):
    #filter is used as where clause in this
                        #table name/model that convert after
                            #  |                        
                            #  |                            WHERE Id == the id comes when 
                            #  |                                 the user passes any id
                            #  |                              id of the product table
                            #  |                         so the query becomes
                            #  |                        SELECT * FROM PRODUCT WHERE ID = 1
                            #  |                      this id is of product table as product.id 
                            #  v                                               and this first means Fetch me the first relevant id
    db_product = db.query(database_models.Product).order_by(database_models.Product.id).filter(database_models.Product.id == id).first() 
    if db_product:
        return db_product
    return {"message":"product not found"}

@app.post("/product")
def add_product(product:Products,db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/product")
def update_product(id:int , product:Products,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    else:
        return {"product not found"}

    
@app.delete("/product/{id}")
def remove_product(id:int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return "product is not found"

