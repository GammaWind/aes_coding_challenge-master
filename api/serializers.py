from rest_framework import serializers



from transaction.models import Transaction, LineItem, InventoryItem


class TransactionSerializer(serializers.ModelSerializer):

    transaction_number = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('__all__')


class InventoryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryItem
        fields = ['line_item', 'article', 'color', 'company',
                  'gross_quantity', 'net_quantity', 'unit']

    


class LineItemSerializer(serializers.ModelSerializer):
    inventory_items = InventoryItemSerializer(many=True, read_only=True)

    class Meta:
        model = LineItem
        fields = ['id', 'article', 'color', 'required_on_date', 'quantity',
                  'rate_per_unit', 'unit', 'transaction_number', 'inventory_items']

    

class GetTransactionSerializer(serializers.ModelSerializer):

    transaction_number = serializers.CharField(read_only=True)
    line_items = LineItemSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['company', 'branch', 'department', 'transaction_number',
                  'transaction_status', 'remarks', 'line_items']
