class User(object):
    """Represent a user in the database, player that has paid for a ticket.

    Args:
        object (_type_): _description_
    """
    
    
    def __init__(self, email, ticket_id):
        self.email = email
        self.ticket_id = ticket_id
        
        