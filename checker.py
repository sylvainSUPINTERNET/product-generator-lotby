import os
import stripe
def check_credentials():
    
    
    if "FREE_IMG_API_KEY" not in os.environ:
        raise Exception("FREE_IMG_API_KEY environment variable not set. Please visit : https://freeimage.host/page/api")
    
    if "STRIPE_SK" not in os.environ:
        raise Exception("STRIPE_SK environment variable not set")
    
    if "STRIPE_PK" not in os.environ:
        raise Exception("STRIPE_PK environment variable not set")
    

    stripe.api_key = os.environ["STRIPE_SK"]

    return stripe
    
