import os
import stripe

def check_credentials():
    
    
    # if "FREE_IMG_API_KEY" not in os.environ:
    #     raise Exception("FREE_IMG_API_KEY environment variable not set. Please visit : https://freeimage.host/page/api")
    
    if "STRIPE_SK" not in os.environ:
        raise Exception("STRIPE_SK environment variable not set")
    
    if "STRIPE_PK" not in os.environ:
        raise Exception("STRIPE_PK environment variable not set")
    

    stripe.api_key = os.environ["STRIPE_SK"]
    
    return stripe
    
def generate_url_for_env(env):
    if env in "test":
        return "https://dashboard.stripe.com/test"
    
    return "https://dashboard.stripe.com"
