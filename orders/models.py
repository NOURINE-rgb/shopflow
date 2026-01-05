from django.db import models

# Create your models here.
    
class Order(models.Model):
    class OrderStatus(models.TextChoices):
       REQUESTED = 'requested', 'Requested'
       CONFIRMED = 'confirmed', 'Confirmed'
       IN_WAY = 'in_way', 'In the way'
       DELIVERED = 'delivered', 'Delivered'
       NOT_DELIVERED = 'not_delivered', 'Not delivered'
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    status = models.CharField(max_length=20, choices = OrderStatus.choices, default=OrderStatus.REQUESTED)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"