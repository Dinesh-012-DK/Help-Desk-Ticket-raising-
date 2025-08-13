from django.urls import path
from .views import *

urlpatterns = [
    path('', sign_in, name='sign_in'),
    
    # -------------------Admin_Dashboard-------------------
    path('Admin_dash', Admin_dashboard, name='Admin_dash'),

    path('create_admin', create_admin, name='create_admin'),
    path('update/<int:admin_id>/', update_admin, name='update_admin'),
    path('delete/<int:admin_id>/', delete_admin, name='delete_admin'),
    
    path('create_agent', create_agent, name='create_agent'),
    path('update_agent/<int:agent_id>/', update_agent, name='update_agent'),
    path('delete_agent/<int:agent_id>/', delete_agent, name='delete_agent'),
    
    path('create_user', create_user, name='create_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('delete_user/<int:user_id>/', delete_user, name= 'delete_user'),
    
    path('admin/ticket_monitoring/', ticket_monitor, name='ticket_monitor'),

    path('assign_ticket/<int:ticket_id>/', assign_ticket, name='assign_ticket'),

    path('admins/profile_update/', profile_update_admin, name='admin_profile_update'),
    
    # -------------------Agent_Dashboard-------------------
    path('Agent_dash', Agent_dashboard, name='Agent_dash'),
    
    path('agent/', assigned_ticket, name='agent_index'),
    path('agent/profile_update/', profile_update_agent, name='agent_profile_update'),
    path('agent/ticket_details/<int:ticket_id>/', update_ticket_status, name='ticket_details'),

    # -------------------User_Dashboard-------------------
    path('User_dash', User_dashboard, name='User_dash'),
    
    path('user/profile_update/', profile_update_user, name='profile_update'),
    path('user/create_ticket/', ticket_raising, name='create_ticket'),
    path('delete_ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('user/feedback/', submit_feedback, name='submit_feedback'),
    
    path('logout', logout_view, name='logout'),
]
