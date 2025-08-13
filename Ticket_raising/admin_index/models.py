from django.db import models

# Create your models here.
class Admin(models.Model):
    admin_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=20)
    admin_id=models.IntegerField()
    
    def __str__(self):
        return self.admin_name
    
class Agent(models.Model):
    agent_name=models.CharField(max_length=100)
    agent_id=models.IntegerField()
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=20)
    
    def __str__(self):
        return self.agent_name
    
class User(models.Model):
    user_name=models.CharField(max_length=100)
    user_id=models.ImageField()
    email=models.EmailField(max_length=100)
    sys_id=models.IntegerField()
    password=models.CharField(max_length=20)
    
    def __str__(self):
        return self.user_name
    
    
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    CATEGORY_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Network', 'Network'),
        ('Other', 'Other'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]
    tracking_data = models.JSONField(null=False, blank=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Low') 
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True) 
    
    seen_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen_by_agent = models.BooleanField(default=False)
    
    
class TicketFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1 - Poor'), (2, '2'), (3, '3 - Okay'), (4, '4'), (5, '5 - Excellent')])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)