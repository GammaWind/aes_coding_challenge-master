from django.urls import path, include
from .controller import Transactions, AddLineItems, AddInventoryItem,GetTransactionDetail





api_urls = [
    
    
    path('transaction/',Transactions.as_view()),
    path('gettransaction/<str:tn>',GetTransactionDetail.as_view()),
    path('deletetransaction/<str:tn>',Transactions.as_view()),
    path('addlineitem/',AddLineItems.as_view()),
    path('addinventoryitem/',AddInventoryItem.as_view()),

]