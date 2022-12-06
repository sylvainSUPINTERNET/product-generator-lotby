

# class CredentialManager(object):
    
#     def __init__(self, stripe_pk, stripe_sk):
#         self.stripe_pk = stripe_pk
#         self.stripe_sk = stripe_sk
        
        
#     def print_credentials(self):
#         print(self.stripe_pk)
        
#         if len(self.stripe_sk) == 0:
#             return Exception("Wrong secret provided")

#         if len(self.stripe_sk) <= 5:
#             print(self.stripe_sk)
#         else:
#             hidden_sk = "".join([ v if i > len(self.stripe_sk) - 5 else '*' for (i, v) in enumerate(self.stripe_sk) ])
#             print(hidden_sk)
            
     
