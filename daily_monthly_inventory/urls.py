from django.urls import path

from daily_monthly_inventory.views import (
    CreateInventoryView,
    DeleteInventoryView,
    GetInventoryDetailView,
    ListAmbulancesView,
    ListInventoryView,
    ListShiftsView,
    UpdateInventoryView,
)

urlpatterns = [
    path("list_inventories/", ListInventoryView.as_view(), name="inventory_list"),
    path("create_inventory/", CreateInventoryView.as_view(), name="create_inventory"),
    path(
        "<int:inventory_id>/get_detail/",
        GetInventoryDetailView.as_view(),
        name="get_inventory_detail",
    ),
    path("list_ambulances/", ListAmbulancesView.as_view(), name="list_ambulances"),
    path("list_shifts/", ListShiftsView.as_view(), name="list_shifts"),
    path(
        "<int:inventory_id>/update_inventory/",
        UpdateInventoryView.as_view(),
        name="update_inventory",
    ),
    path(
        "<int:inventory_id>/delete_inventory/",
        DeleteInventoryView.as_view(),
        name="delete_inventory",
    ),
]
