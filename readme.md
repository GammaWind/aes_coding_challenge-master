
Transaction Number format: 
TRN-{Count}-{Year}
eg. TRN-1-2021

Endpoints:
1. Add new transaction
POST : api/transaction/

2. Delete Transaction
DELETE : api/deletetransaction/<str:tn>
tn - transaction number


3. Add LineItem
POST : api/addlineitem/

4. Add InventoryItem
POST : api/addinventoryitem/

5. Get Transaction Detail:
GET : api/gettransaction/<str:tn>
tn - transaction  number


