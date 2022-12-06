import click


from checker import check_credentials
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

def create_product_stripe(name, description, image_url, shippable, statement_descriptor, remove_image_background):
    
    try:
        # https://stripe.com/docs/tax/tax-categories
        tax_code = "txcd_99999999"
        unit_label = name
        stripe = check_credentials()
        download_picture(image_url)
        if remove_image_background:
            proccess_image()
        
        product = stripe.Product.create(
            name=name,
            description=description,
            images=[image_url],
        )

        

        
        
    except Exception as e :
        print(e)

    
    





if __name__ == "__main__":
    app()

