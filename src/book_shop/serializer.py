from rest_framework import serializers
from book_shop.models import Author, Publisher, Book, OrderItem, Order


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.authors.set(self.initial_data.get('authors', []))
        instance.publishers.set(self.initial_data.get('publishers', []))
        return instance

    def update(self, instance, validated_data):
        authors = self.initial_data.pop('authors')
        publishers = self.initial_data.pop('publishers')

        if authors != None:
            instance.authors.clear()
            instance.authors.set(authors)
        if publishers != None:
            instance.publishers.clear()
            instance.publishers.set(publishers)
        instance = super().update(instance, validated_data)
        return instance


class OrderBookSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='book.id')
    name = serializers.ReadOnlyField(source='book.name')
    cost = serializers.ReadOnlyField(source='book.cost')
    books_cost = serializers.ReadOnlyField(source='get_cost')

    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'cost', 'quantity', 'books_cost')


class OrderSerializer(serializers.ModelSerializer):
    books = OrderBookSerializer(source='orderitem_set', many=True, read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    order_price = serializers.ReadOnlyField(source='get_total_cost')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        for item in self.initial_data.get('books', []):
            instance.books.add(item.pop('book'), through_defaults=item)
        return instance

    def update(self, instance, validated_data):
        validated_data['status'] = self.initial_data['status']
        instance = super().update(instance, validated_data)
        if self.initial_data.get('books') != None:
            instance.books.clear()
            for item in self.initial_data.get('books'):
                instance.books.add(item.pop('book'), through_defaults=item)
        return instance
