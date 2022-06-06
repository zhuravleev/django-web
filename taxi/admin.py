from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from .models import User, Car, Driver, Order

@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    class Meta:
        proxy = True

@admin.register(Car)
class CarAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    class Meta:
        proxy = True

@admin.register(Driver)
class DriverAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    class Meta:
        proxy = True

@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    class Meta:
        proxy = True
