import datetime

class Product(object):
    """Represents a product in the database associated to one ticket/price from Stripe.

    Args:
        object (_type_): _description_
    """
    def __init__(self, name, ticket_id, ticket_price_id, price, end_at):
        self.name = name
        self.ticket_id = ticket_id
        self.ticket_price_id = ticket_price_id
        self.price=price
        self.created_at = datetime.datetime.now().isoformat()
        self.end_at = end_at # ISO format