# from transaction.models import Transaction
# from datetime import date


# def GenerateTransactionNumber():
#     last_transaction = Transaction.object.all().last().transaction_number
#     spl = last_transaction.split('/')
#     number = int(spl[1])
#     number += 1
    
#     year = spl[2]

#     current_year = date.today().year

#     if int(current_year) > int(year):
#         return 'TRN/' + '1/' + str(current_year)
#     else:
#         return 'TRN/' + str(number) + '/' + str(current_year)   

    
    


# GenerateTransactionNumber()