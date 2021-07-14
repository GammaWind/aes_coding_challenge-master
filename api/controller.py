from django.shortcuts import render
from rest_framework import generics, response, status
from .serializers import TransactionSerializer, LineItemSerializer, InventoryItemSerializer, GetTransactionSerializer
from transaction.models import Transaction, LineItem, InventoryItem


class Transactions(generics.GenericAPIView):
    serializer_class = TransactionSerializer

    def post(self, request, *kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return response.Response({"transaction": TransactionSerializer(transaction, context=self.get_serializer_context()).data})

    def delete(self, request, tn, *kwargs):

        transaction = None
        try:
            transaction = Transaction.objects.get(transaction_number=tn)
        except Transaction.DoesNotExist:
            response.Response.status_code = status.HTTP_404_NOT_FOUND
            return response.Response({"message": "does not exist", "status": status.HTTP_404_NOT_FOUND})

        #check if there are LineItems/InventoryItems

        line_items = LineItem.objects.filter(transaction_number=tn)

        total_inventory_items = []

        for i in line_items:
            inventory_items = InventoryItem.objects.filter(line_item=i.id)
            total_inventory_items += inventory_items

        if not total_inventory_items:
            transaction.delete()
            response.Response.status_code = status.HTTP_200_OK
            return response.Response({"message": 'Transaction deleted successfully', "status": status.HTTP_200_OK})

        response.Response.status_code = status.HTTP_400_BAD_REQUEST
        return response.Response({"message": 'transaction cannot be deleted as transaction has inventory items added', "status": status.HTTP_400_BAD_REQUEST})


class GetTransactionDetail(generics.GenericAPIView):
    serializer_class = GetTransactionSerializer

    def get(self, request, tn, *kwargs):
        transaction = None
        try:
            transaction = Transaction.objects.get(transaction_number=tn)
        except Transaction.DoesNotExist:
            response.Response.status_code = status.HTTP_404_NOT_FOUND
            return response.Response({"message": "does not exist", "status": status.HTTP_404_NOT_FOUND})

        response.Response.status_code = status.HTTP_200_OK
        return response.Response({"Data": GetTransactionSerializer(transaction, context=self.get_serializer_context()).data, "message": "success", "status": status.HTTP_200_OK})


class AddLineItems(generics.GenericAPIView):
    serializer_class = LineItemSerializer

    def post(self, request, *kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        line_item = serializer.save()
        response.Response.status_code = status.HTTP_201_CREATED
        return response.Response({"data": LineItemSerializer(line_item, context=self.get_serializer_context()).data, "message": "success", "status": status.HTTP_201_CREATED})


class AddInventoryItem(generics.GenericAPIView):
    serializer_class = InventoryItemSerializer

    def post(self, request, *kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inventory_item = serializer.save()

        response.Response.status_code = status.HTTP_201_CREATED
        return response.Response({"data": InventoryItemSerializer(inventory_item, context=self.get_serializer_context()).data, "message": "success", "status": status.HTTP_201_CREATED})
