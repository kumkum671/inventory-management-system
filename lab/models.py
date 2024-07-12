from django.db import models
from core.models import UserProfile
from org.models import Org, Department


class Lab(models.Model):
    user = models.ManyToManyField(UserProfile)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=255)
    room_no = models.IntegerField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{str(self.lab_name)} | {str(self.room_no)}"
    

class LabSettings(models.Model):
    lab = models.OneToOneField(Lab, on_delete=models.CASCADE)
    items_tab = models.BooleanField(default=False)
    sys_tab = models.BooleanField(default=False)
    categories_tab = models.BooleanField(default=False)
    brands_tab = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.lab.lab_name} Settings"
    

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.category_name)
    

class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=True, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.brand_name)


class Item(models.Model):
    unique_code = models.CharField(max_length=5, unique=True)
    item_name = models.CharField(max_length=255)
    total_qty = models.IntegerField(default=1)
    in_use_qty = models.IntegerField(default=0)
    total_available_qty = models.IntegerField(default=0)
    removed_qty = models.IntegerField(default=0)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    date_of_purchase = models.DateField()
    
    def __str__(self):
        return str(self.item_name)
    
    
class System(models.Model):
    unique_code = models.CharField(max_length=5, unique=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    sys_name = models.CharField(max_length=255, verbose_name="System Name")

    # Components (consider using a generic relation)
    components = models.ManyToManyField(
        Item, related_name='systems', through='SystemComponent'
    )

    # System status with a custom manager for filtering/reporting
    STATUS_CHOICES = [
        ("working", "Working"),
        ("not_working", "Not working"),
        ("item_missing", "Item missing"),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, blank=False, null=False)

    # Additional fields for tracking/reporting (optional)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class SystemComponent(models.Model):
    system = models.ForeignKey(System, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=255)
    COMPONENT_TYPES = [
        ("mouse", "Mouse"),
        ("keyboard", "Keyboard"),
        ("processor", "Processor"),
        ("ram", "RAM"),
        ("storage", "HDD/SSD"),
        ("os", "Operating System"),
        ("monitor", "Monitor"),
        ("cpu_cabin", "CPU Cabin"),
    ]
    component_type = models.CharField(max_length=255, choices=COMPONENT_TYPES)


class LabRecord(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    log_text = models.CharField(max_length=500)
    user_desc = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.lab)
