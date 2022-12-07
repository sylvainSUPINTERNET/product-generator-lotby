import logging
logging.basicConfig(level = logging.INFO)

import click
import pathlib

from checker import check_credentials, generate_url_for_env
from service import download_picture, proccess_image

# API descriptor Stripe
# https://www.postman.com/stripedev/workspace/stripe-developers/request/665823-8380209d-f228-4f74-bb79-ee811ee37033

@click.group()
def app():
    """Product generator for stripe, made by sylvain for lotby"""


@app.command(name="create-product")
@click.option("--name", prompt="Name", required=True)
@click.option("--description", prompt="Description", required=True)
@click.option("--image_url", prompt="Url image", required=True)
@click.option("--shippable", prompt="Shippable", default=True, required=True)
@click.option("--statement_descriptor", prompt="Name on bank statement", required=True)
@click.option("--remove_image_background", prompt="Remove image background",default=True, required=True)
@click.option("--unit_amount_decimal", prompt="Montant decimal", required=True)
@click.option("--currency", prompt="Currency (https://www.iso.org/iso-4217-currency-codes.html)", default="eur", required=True)

def create_product_stripe(name, description, image_url, shippable, statement_descriptor, remove_image_background, unit_amount_decimal, currency):

    try:
        PIC_NO_BG_NAME="tmp-no-bg.jpg"
        
        # https://stripe.com/docs/tax/tax-categories
        tax_code = "txcd_99999999"
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
        
        logging.info(f"Price created {price.id} and associated to product {product.name} - {product.id}")
        
        
        logging.info(f"You can find it here : {generate_url_for_env(env=ctx)}/products")
        logging.info(f" > Don't forget to add image ( no background ) on stripe dashboard: {pathlib.Path(__file__).parent.resolve()}\dis\{PIC_NO_BG_NAME}")
        
        
        
        

    except Exception as e :
        print(e)

   
if __name__ == "__main__":
    app()

