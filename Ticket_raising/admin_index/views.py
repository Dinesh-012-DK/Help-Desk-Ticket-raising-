from django.shortcuts import render, redirect
from django.contrib import messages
from requests import get
from .models import *
from .models import Ticket
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
# Create your views here.

# --------------------------------------Create_Admin------------------------------------------#
def create_admin(request):
    if request.method == 'POST':
        admin = request.POST.get('admin_name')
        email = request.POST.get('admin_email')
        password = request.POST.get('admin_pass')
        admin_id = request.POST.get('admin_id')
        
        
        if admin and email and password and admin_id:
            if Admin.objects.filter(admin_name=admin).exists():
                messages.error(request, f"Username '{admin}' already exists.")
                return redirect('Admin_dash')
            elif Admin.objects.filter(admin_id=admin_id).exists():
                messages.error(request, f"Admin_id '{admin_id}' already exists.")
                return redirect('Admin_dash')
            elif Admin.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists.")
                return redirect('Admin_dash')
            
            else:
                Admin.objects.create(
                    admin_name=admin,
                    email=email,
                    password=password,
                    admin_id=admin_id,
                )
                
                messages.success(request, f"Admin {admin} created successfully.")
                return redirect('Admin_dash')  
        else:
            messages.error(request, 'All fields are required')
            return redirect('Admin_dash')

    return render(request, 'Dashboard/Admin_dashboard.html')

# --------------------------------------Create_Agent------------------------------------------#
def create_agent(request):
    if request.method == 'POST':
        agent = request.POST.get('agent_name')
        emp = request.POST.get('agent_id')
        email = request.POST.get('agent_email')
        password = request.POST.get('agent_pass')
        
        if agent and emp and email and password:
            if Agent.objects.filter(agent_name=agent).exists():
                messages.error(request, f"Username '{agent}' already exists.")
                return redirect('Admin_dash')
            elif Agent.objects.filter(agent_id=emp).exists():
                messages.error(request, f"Agent_id '{emp}' already exists.")
                return redirect('Admin_dash')
            elif Agent.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists.")
                return redirect('Admin_dash')
            else:
                Agent.objects.create(
                    agent_id=emp,
                    agent_name=agent,
                    email=email,
                    password=password,
                )
                messages.success(request, f"Agent {agent} created successfully.")
                return redirect('Admin_dash')
        else:
            messages.error(request, 'All fields are required') 
            return redirect('Admin_dash')           

    return render(request, 'Dashboard/Admin_dashboard.html')


# --------------------------------------Create_User------------------------------------------#
def create_user(request):
    if request.method == 'POST':
        user = request.POST.get('user_name')
        user_id = request.POST.get('user_id')
        email = request.POST.get('user_email')
        sys_id=request.POST.get('system_id')
        password = request.POST.get('user_pass')
        
        if user and user_id and email and sys_id and password:
            if User.objects.filter(user_name=user).exists():
                messages.error(request, f"Username '{user}' already exists.")
                return redirect('Admin_dash')
            elif User.objects.filter(user_id=user_id).exists():
                messages.error(request, f"user_id '{user_id}' already exists.")
                return redirect('Admin_dash')
            elif User.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists.")
                return redirect('Admin_dash')
            elif User.objects.filter(sys_id=sys_id).exists():
                messages.error(request, f"System_Id '{sys_id}' already exists.")
                return redirect('Admin_dash')
            else:
                User.objects.create(
                    user_name=user,
                    user_id=user_id,
                    email=email,
                    sys_id=sys_id,
                    password=password,
                )
                messages.success(request, f"User {user} created successfully.")
                return redirect('Admin_dash')
        else:
            messages.error(request, 'All fields are required')
            return redirect('Admin_dash')

    return render(request, 'Dashboard/Admin_dashboard.html')


# --------------------------------------Role-Based_Sign_In------------------------------------------#
def sign_in(request):
    # global admin
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('user')
        password = request.POST.get('password')
        
        
        # Input validation
        if not role or not username or not password:
            messages.error(request, 'All fields are required')
            return render(request, 'Auth/login.html')


        # Role-based authentication
        if role == 'Admin':
            admin = Admin.objects.filter(admin_name=username).first()
            if admin and admin.password == password:
                request.session['admin_name'] = admin.admin_name
                messages.success(request, f'Welcome Admin, {username} 😎')
                return redirect('Admin_dash')
            else:
                messages.error(request, 'Invalid Admin')


        elif role == 'Agent':
            agent = Agent.objects.filter(agent_name=username).first()
            if agent and agent.password == password:
                request.session['agent_name'] = agent.agent_name 
                messages.success(request, f'Welcome Agent, {username} 😇')
                return redirect('Agent_dash')  
            else:
                messages.error(request, 'Invalid Agent')
        
        
        elif role == 'User':
            user = User.objects.filter(user_name=username).first()
            if user and user.password == password:
                request.session['user_name'] = user.user_name
                messages.success(request, f'Welcome User, {username} 👋')
                return redirect('User_dash')  
            else:
                messages.error(request, 'Invalid User')

    return render(request, 'Auth/login.html' )

#--------------------------------------Password_Seen------------------------------------------#
def mark_tickets_seen(request):
    if request.method == "POST" and request.session.get('admin_name'):
        Ticket.objects.filter(seen_by_admin=False).update(seen_by_admin=True)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})

#--------------------------------------Logout_Admin------------------------------------------#
def logout_view(request):
    # Clear session data
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('sign_in')

#--------------------------------------Update_Admin------------------------------------------#
def update_admin(request, admin_id):
    all_admins = Admin.objects.all().order_by('id')
    try:
        admin = Admin.objects.get(id=admin_id)
        if request.method == 'POST':
            admin.admin_name = request.POST.get('admin_name')
            admin.email = request.POST.get('admin_email')
            admin.password = request.POST.get('admin_pass')
            admin.admin_id = request.POST.get('admin_id')
            admin.save()
            messages.success(request, f"Admin {admin.admin_name} updated successfully.")
            return redirect('Admin_dash')
        return render(request, 'Dashboard/Admin_dashboard.html', {'admins': all_admins , })
    except Admin.DoesNotExist:
        messages.error(request, f'Admin not found')
        return redirect('Admin_dash')

#---------------------------------------Delete_Admin------------------------------------------#

def delete_admin(request, admin_id):
    admin = Admin.objects.count() == 1
    if admin == 1:
        messages.error(request, "You cannot delete the last admin.")
        return redirect('Admin_dash')
    
    admin = get_object_or_404(Admin, id=admin_id)
    
    # if request.user.id == admin.id:
    #     request.session.flush() 

    admin_name = admin.admin_name
    admin.delete()
    messages.success(request, f"Admin '{admin_name}' deleted successfully.")
    
    return redirect('Admin_dash')
    
    # admin = Admin.objects.count() == 1
    # if admin == 1:
    #     messages.error(request, "You cannot delete the last admin.")
    #     return redirect('Admin_dash')
    # try:
    #     admin = Admin.objects.get(id=admin_id)
    #     admin.delete()
    #     messages.success(request, f'Admin {admin.admin_name} deleted successfully')
    # except Admin.DoesNotExist:
    #     messages.error(request, f'Admin not found')

    # return redirect('Admin_dash')


#--------------------------------------Update_Agent------------------------------------------#

def update_agent(request, agent_id):
    all_agents = Agent.objects.all().order_by('id')
    if Agent.objects.count() == 1:
        messages.error(request, "You cannot update the last user.")
        return redirect('Admin_dash') 
    try:
        agent = Agent.objects.get(id=agent_id)
        if request.method == 'POST':
            agent.agent_name = request.POST.get('agent_name')
            agent.email = request.POST.get('agent_email')
            agent.password = request.POST.get('agent_pass')
            agent.agent_id = request.POST.get('agent_id')
            agent.save()
            messages.success(request, f"Agent {agent.agent_name} updated successfully.")
            return redirect('Admin_dash')
        return render(request, 'Dashboard/Admin_dashboard.html', {'agents': all_agents , })
    except Agent.DoesNotExist:
        messages.error(request, f'Agent not found')
        return redirect('Admin_dash')


#---------------------------------------Delete_Agent------------------------------------------#

def delete_agent(request, agent_id):
    agent = Agent.objects.count() == 1
    if agent == 1:
        messages.error(request, "You cannot delete the last agent.")
        return redirect('Admin_dash')

    agent = get_object_or_404(Agent, id=agent_id)

    if request.user.id == agent.id:
        request.session.flush() 

    agent_name = agent.agent_name
    agent.delete()
    messages.success(request, f"Agent '{agent_name}' deleted successfully.")
    
    return redirect('Admin_dash')

#--------------------------------------Update_User------------------------------------------#

def update_user(request, user_id):
    all_users = User.objects.all().order_by('id')
      
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            user.user_name = request.POST.get('user_name')
            user.email = request.POST.get('user_email')
            user.password = request.POST.get('user_pass')
            user.sys_id = request.POST.get('user_sys_id')
            user.user_id = request.POST.get('user_id')
            user.save()
            messages.success(request, f"User {user.user_name} updated successfully.")
            return redirect('Admin_dash')
        return render(request, 'Dashboard/Admin_dashboard.html', {'users': all_users })
    except User.DoesNotExist:
        messages.error(request, f'User not found')
        return redirect('Admin_dash')

#---------------------------------------Delete_User------------------------------------------#

def delete_user(request, user_id):
    user = User.objects.count() == 1
    if user == 1:
        messages.error(request, "You cannot delete the last user.")
        return redirect('Admin_dash')

    user = get_object_or_404(User, id=user_id)

    if request.user.id == user.id:
        request.session.flush() 

    user_name = user.user_name
    user.delete()
    messages.success(request, f"User '{user_name}' deleted successfully.")
    
    return redirect('Admin_dash')

#-----------------------------------------Admin-----------------------------------------------#
#------------------------------------Admin_Dashboard------------------------------------------#
def Admin_dashboard(request):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')

    adminname = request.session['admin_name']
    adminshow = Admin.objects.get(admin_name=adminname)

    tickets = Ticket.objects.all().order_by('-created_at')

    Ticket.objects.filter(seen_by_admin=False).update(seen_by_admin=True)

    unseen_ticket_count = Ticket.objects.filter(seen_by_admin=False).count()
    
    admin_all=Admin.objects.all().order_by('-id')
    agent_all=Agent.objects.all().order_by('-id')
    user_all=User.objects.all().order_by('-id')
    feedbacks = TicketFeedback.objects.select_related('user').order_by('-created_at')
    
    return render(request, 'Dashboard/Admin_dashboard.html', {
        'admin': adminname,
        'adminshow': adminshow,
        'admins':admin_all,
        'agents':agent_all,
        'users':user_all,
        'tickets': tickets,
        'feedbacks': feedbacks,
        'unseen_ticket_count': unseen_ticket_count,
        })


def ticket_monitor(request):
    if 'admin_name' not in request.session:
        messages.error(request, "Admin not logged in.")
        return redirect('sign_in')

    adminname = request.session['admin_name']
    
    all_agents = Agent.objects.all()
    all_admins = Admin.objects.all().order_by('id')
    all_users = User.objects.all().order_by('id')
    
    tickets = Ticket.objects.all().order_by('created_at')

    Ticket.objects.filter(seen_by_admin=False).update(seen_by_admin=True)

    unseen_ticket_count = Ticket.objects.filter(seen_by_admin=False).count()

    return render(request, 'Dashboard/Admin_dashboard.html', 
                  {'tickets': tickets,
                   'section': 'ticket_monitor',
                   'all_agents': all_agents,
                    'all_admins':all_admins,
                    'all_users':all_users,
                    'admin_name':adminname,
                    'unseen_ticket_count': unseen_ticket_count,
                   })
    
    
def assign_ticket(request, ticket_id):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin not logged in.')
        return redirect('sign_in')

    adminname = request.session['admin_name']
    print("Admin Name:", adminname)
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    all_agents = Agent.objects.all()
    all_admins = Admin.objects.all().order_by('-id')
    all_users = User.objects.all().order_by('-id')
    tickets = Ticket.objects.all().order_by('-created_at')
    
    print("Ticket ID:", ticket_id)
    
    if request.method == 'POST':
        assign_agent = request.POST.get('assign_agent')
        print(assign_agent)
        
        if assign_agent:  
            agent = get_object_or_404(Agent, agent_name=assign_agent)
            print("Assigned Agent:", agent)
            ticket.assigned_agent = agent
            ticket.status = 'In Progress'
            ticket.is_seen_by_agent = False
            ticket.save()
            print("Ticket after assignment:", ticket)
            messages.success(request, f"Ticket assigned to {agent.agent_name}")
            return redirect('Admin_dash')  
        else:
            messages.error(request, "No agent selected.")

    return render(request, 'Admin/Admin_dashboard.html', {
        'ticket': ticket,
        'tickets': tickets,
        'all_agents': all_agents,
        'section': 'assign_ticket',
        'all_admins': all_admins,
        'all_users': all_users,
        'admin_name': adminname
    })

#----------------------------------Admin-profile-update----------------------------------#

def profile_update_admin(request):
    # Check if session exists
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')

    username = request.session['admin_name']
    
    admin = get_object_or_404(Admin, admin_name=username)

    if request.method == 'POST':
        admin.admin_name = request.POST.get('admin_name')
        admin.email = request.POST.get('admin_email')
        admin.password = request.POST.get('password') 
        admin.save()

        request.session['admin_name'] = admin.admin_name
        messages.success(request, f'User {admin.admin_name} updated successfully')
        return redirect('Admin_dash')

    all_admin = Agent.objects.all().order_by('-id')
    tickets = Ticket.objects.filter(agent=admin).order_by('-created_at')

    return render(
        request,
        'Dashboard/Admin_dashboard.html', 
        {
            'user_name': admin.admin_name,
            'all_users': all_admin,
            'user': admin,
            'tickets': tickets
        }
    )

#-------------------------------------------Agent-----------------------------------------------#
#--------------------------------------Agent_Dashboard------------------------------------------#

def Agent_dashboard(request):
    if 'agent_name' not in request.session:
        messages.error(request, 'Agent session was not created')
        return redirect('sign_in')
    
    agent_name = request.session['agent_name']
    agent = Agent.objects.get(agent_name=agent_name)

    # All tickets assigned to this agent
    assigned_tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')

    # If you want a specific ticket's details for the modal
    ticket_details = None
    if assigned_tickets.exists():
        ticket_details = assigned_tickets.first()  # Or choose based on your logic

    return render(request, 'Dashboard/Agent_dashboard.html', {
        'agent_name': agent_name,
        'agent': agent,
        'assigned_tickets': assigned_tickets,
        'ticket_details': ticket_details,  # Pass to template for modal
    })


# Assigned Ticket 
def assigned_ticket(request):
    if 'agent_name' not in request.session:
        messages.error(request, "Agent not logged in.")
        return redirect('sign_in')
    
    agent_name = request.session['agent_name'] 
    
    agent = Agent.objects.get(agent_name=agent_name)
    
    tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')
    all_users = User.objects.all().order_by('-id')
    
    Ticket.objects.filter(assigned_agent=agent, is_seen_by_agent=False).update(is_seen_by_agent=True)
    assigned_tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')
    unseen_count = Ticket.objects.filter(assigned_agent=agent, is_seen_by_agent=False).count()
    
    return render(request, 'Dashboard/Agen_dashboard.html', {
        'assigned_tickets': tickets,  
        'section': 'Ticket-Dashboard',
        'agent_name': agent_name,
        'tickets': assigned_tickets,
        'agent': agent,
        'all_users': all_users,
        'unseen_count': unseen_count,
    })
    
    
def profile_update_agent(request):
    if 'agent_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')

    username = request.session['agent_name']
    
    agent = get_object_or_404(Agent, agent_name=username)

    if request.method == 'POST':
        agent.agent_name = request.POST.get('agent_name')
        agent.email = request.POST.get('agent_email')
        agent.password = request.POST.get('password') 
        agent.save()
        
        request.session['agent_name'] = agent.agent_name
        messages.success(request, f'Agent {agent.agent_name} updated successfully')
        return redirect('Agent_dash')

    return render(request,'Dashboard/Agent_dashboard.html',{
            'user_name': agent.agent_name,
            'agent': agent,
        }
    )
    
def update_ticket_status(request, ticket_id):
    if 'agent_name' not in request.session:
        messages.error(request, "Agent not logged in.")
        return redirect('sign_in')
    
    agent_name = request.session['agent_name']
    
    agent = Agent.objects.get(agent_name=agent_name)

    ticket = get_object_or_404(Ticket, id=ticket_id, assigned_agent=agent)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        ticket.status = new_status
        ticket.save()
        messages.success(request, f"Ticket raised by {ticket.user.user_name} in system no. {ticket.user.sys_id} is {new_status}")
        return redirect('Agent_dash')
     
    return render(request, 'Dashboard/Agent_dashboard.html', {
        'ticket': ticket,
        'agent_name': agent_name,
        'section': 'Ticket-Dashboard',
        'agent': agent,
    })


#--------------------------------------------User-----------------------------------------------#
#---------------------------------------User_Dashboard------------------------------------------#

def User_dashboard(request):
    if 'user_name' not in request.session:
        messages.error(request, 'User session was not created')
        return redirect('sign_in')
    
    username = request.session['user_name']
    user = get_object_or_404(User, user_name=username)
    tickets = Ticket.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'Dashboard/User_dashboard.html', {
        'user': user,
        'tickets': tickets,
    })


def ticket_raising(request):
    if 'user_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')

    username = request.session['user_name']
    user = get_object_or_404(User, user_name=username)

    tickets = Ticket.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('ticket_title')
        description = request.POST.get('ticket_description')
        attachment = request.FILES.get('image')
        category = request.POST.get('ticket_category')
        priority = request.POST.get('ticket_priority')

        if not all([title, description, category, priority]):
            messages.error(request, "All fields are required!")
            return redirect('create_ticket')

        ticket = Ticket(
            title=title,
            description=description,
            user=user,
            category=category,
            priority=priority,
            seen_by_admin=False
        )

        if attachment:
            ticket.attachment = attachment

        ticket.save()
        messages.success(request, 'Ticket raised successfully!!!')
        return redirect('create_ticket')

    return render(request, 'Dashboard/User_dashboard.html', {'user': user, 'tickets': tickets})


def track_ticket(request):
    if 'user_name' not in request.session:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('sign_in')
    try:
        username = request.session['user_name']
        user = User.objects.get(user_name=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('sign_in')

    tickets = Ticket.objects.filter(user=user).order_by('-created_at')
    return render(request, 'dashboard/User_dashboard.html', {'user': user, 'tickets': tickets})


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
    return redirect('create_ticket')


def ticket_history_view(request):
    tickets = Ticket.objects.all().order_by('-created_at')  
    return render(request, 'dashboard/User_dashboard.html', {'datas': tickets})


def submit_feedback(request):
    if 'user_name' not in request.session:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('sign_in')

    username = request.session['user_name']
    user = get_object_or_404(User, user_name=username)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            TicketFeedback.objects.create(
                user=user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Thanks for your feedback!")
        else:
            messages.error(request, 'All fields are required.')
        return redirect('User_dash')

    return render(request, 'dashboard/User_dashboard.html')


def profile_update_user(request):
    # Check if session exists
    if 'user_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')

    username = request.session['user_name']

    user = get_object_or_404(User, user_name=username)

    if request.method == 'POST':
        user.user_name = request.POST.get('user_name')
        user.email = request.POST.get('user_email')
        user.password = request.POST.get('password') 
        user.save()
        
        request.session['user_name'] = user.user_name
        
        messages.success(request, f'User {user.user_name} updated successfully')
        return redirect('User_dash')

    all_users = User.objects.all().order_by('-id')
    tickets = Ticket.objects.filter(user=user).order_by('-created_at')

    return render(
        request,
        'Dashboard/User_dashboard.html', 
        {
            'user_name': user,
            'all_users': all_users,
            'user': user,
            'tickets': tickets
        }
    )