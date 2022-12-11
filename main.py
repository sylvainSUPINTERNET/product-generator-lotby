import logging
from dotenv import load_dotenv
import os
from pprint import pprint
from datetime import timedelta, datetime

load_dotenv()

logging.basicConfig(level = logging.INFO)
from pymongo import MongoClient

import click
import pathlib

from checker import check_credentials, generate_url_for_env
from service import download_picture, proccess_image

from models.Product import Product

# API descriptor Stripe
# https://www.postman.com/stripedev/workspace/stripe-developers/request/665823-8380209d-f228-4f74-bb79-ee811ee37033


dbClient = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))["lotby"]





@click.group()
def app():
    """Product generator for stripe, made by sylvain for lotby"""

@app.command(name="create-product")
@click.option("--name", prompt="Name", required=True)
@click.option("--description", prompt="Description", required=True)
@click.option("--image_url", prompt="Url image", required=True)
@click.option("--shippable", prompt="Shippable", default=True, required=True)
@click.option("--statement_descriptor", prompt="Name on bank statement (5chars)", required=True, )
@click.option("--remove_image_background", prompt="Remove image background",default=True, required=True)
@click.option("--unit_amount_decimal", prompt="Montant decimal (entry ticket price)", required=True)
@click.option("--currency", prompt="Currency (https://www.iso.org/iso-4217-currency-codes.html)", default="eur", required=True)
@click.option("--tax_code", prompt="tax code (https://stripe.com/docs/tax/tax-categories)", default="txcd_99999999", required=True)
@click.option("--total_product_price", prompt="Product price total", required=True)
@click.option("--days_before_game_end_at", prompt="Number of day from today", default=5, required=True)
def create_product_stripe(name, description, image_url, shippable, statement_descriptor, remove_image_background, unit_amount_decimal, currency, tax_code, total_product_price, days_before_game_end_at):
    
    """ Create product and associated price in stripe ( ticket & price ) and also reference in database. Will also generate a picture ready to be used in dashbaord ( ticket or product or product+ticket)
    
    """
    try:
        PIC_NO_BG_NAME="tmp-no-bg.jpg"
        PIC_NO_BG_NAME_WITH_TICKET="tmp-no-bg-ticket.jpg"

        unit_label = name
        
        stripe = check_credentials()
        
        ctx = ""
        if "_test_" in stripe.api_key:
            ctx = "test"
        else:
            ctx = "prod"
        logging.info(f"Context stripe : {ctx}")
        
        
        download_picture(image_url)
        if remove_image_background:
            proccess_image()

        
        # this is the ticket
        product = stripe.Product.create(
            name=name,
            description=description,
            images=[f"./dist/{PIC_NO_BG_NAME}"], # Is not uploading for some reason, do it manually after generation on stripe dashboard ...
            shippable=shippable,
            statement_descriptor=statement_descriptor,
            tax_code=tax_code,
            unit_label=unit_label
        )
        
        logging.info(f"Product created : {product.id}")

        price = stripe.Price.create(
            product=product.id,
            unit_amount_decimal=unit_amount_decimal,
            currency=currency # https://www.iso.org/iso-4217-currency-codes.html
        )
        
        logging.info(f"Price created {price.id} and associated to product {product.name} - {product.id} in stripe")
        logging.info(f"You can find it here : {generate_url_for_env(env=ctx)}/products")
        logging.info(f" > Don't forget to add image ( no background ) on stripe dashboard: {pathlib.Path(__file__).parent.resolve()}\dist\{PIC_NO_BG_NAME}")
        logging.info(f" > Don't forget to add image product ( with ticket ) ( no background ) on stripe dashboard: {pathlib.Path(__file__).parent.resolve()}\dist\{PIC_NO_BG_NAME_WITH_TICKET}")
        
        
        logging.info("Saving product in database ...")
        end_date = datetime.now() + timedelta(days=int(days_before_game_end_at))
        
        product_db = Product(name=name, ticket_id=product.id , ticket_price_id=price.id, price=total_product_price, end_at=end_date.isoformat())
        pid = dbClient["products"].insert_one(product_db.__dict__).inserted_id
        logging.info(f"Product saved in database : {pid}")
    

    except Exception as e :
        print(e)


@app.command(name="list-product")
def delete_product_stripe():
    stripe = check_credentials()
    
    ctx = ""
    if "_test_" in stripe.api_key:
        ctx = "test"
    else:
        ctx = "prod"
        
    logging.info(f"Context stripe : {ctx}")
    
    list_products = [ f"{product['id']} - ( {product['name']} )" for product in stripe.Product.list().data ]
    
    pprint(list_products)
    
    

@app.command(name="list-price")
def delete_product_stripe():
    stripe = check_credentials()
    
    ctx = ""
    if "_test_" in stripe.api_key:
        ctx = "test"
    else:
        ctx = "prod"
        
    logging.info(f"Context stripe : {ctx}")
    
    list_prices = [ f"{price['id']} - ( {price['product']} )" for price in stripe.Price.list().data ]
    
    pprint(list_prices)
    

@app.command(name="delete-product")
@click.option("--product_id", prompt="stripe product ID, will delete stripe price/ticket and db product", required=True, type=str)
def delete_product_stripe(product_id):
    """ Remove product from stripe and database ( ticket and price associated in stripe and remove the product reference in database )
    """
    try:
        stripe = check_credentials()
    
        ctx = ""
        if "_test_" in stripe.api_key:
            ctx = "test"
        else:
            ctx = "prod"
        logging.info(f"Context stripe : {ctx}")
        
        # TODO => make price not active instead of deleting it
        # then delete it from panel ... # https://github.com/stripe/stripe-python/issues/658
        
        # ticket = stripe.Product.retrieve(product_id)
        # ticket_price = stripe.Price.list(product=product_id).data
        
        # Can't delete a price !
        
        # for price in ticket_price:
        #     stripe.Price.delete(price.id)
        #     logging.info(f"Price {price.id} deleted")
            
        stripe.Product.delete(product_id)
        logging.info(f"Ticket {product_id} deleted")
        
        dbClient["products"].delete_one({"ticket_id": product_id})
        logging.info(f"Product {product_id} deleted from database")
        
        logging.info(f"You can delete the associated price : {generate_url_for_env(env=ctx)}/prices")
        
    except Exception as e:
        print(e)


   
if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(e)

