from django.urls import path
from daily_monthly_inventory.views import (
    ListInventoryView,
    CreateInventoryView,
    GetInventoryDetailView
)

urlpatterns = [
    path('list_inventories/', ListInventoryView.as_view(), name='inventory_list'),
    path('create_inventory/', CreateInventoryView.as_view(), name='create_inventory'),
    path('<int:inventory_id>/get_detail/', GetInventoryDetailView.as_view(), name='get_inventory_detail'),
]
