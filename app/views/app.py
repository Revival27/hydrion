import json
import os
import csv
import datetime
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from guardian.shortcuts import get_objects_for_user

from nodeodm.models import ProcessingNode
from app.models import Project, Task, HydroProject, ProjectStatus, HydroTask, Team, HydroSurvey, TaskStatus, TeamMember, Report
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django import forms
from webodm import settings
from app.models.modelform import HydroSurveyForm
import matplotlib.pyplot as plt
import base64
import io


def index(request):
    # Check first access
    if User.objects.filter(is_superuser=True).count() == 0:
        if settings.SINGLE_USER_MODE:
            # Automatically create a default account
            User.objects.create_superuser('admin', 'admin@localhost', 'admin')
        else:
            # the user is expected to create an admin account
            return redirect('welcome')

    if settings.SINGLE_USER_MODE and not request.user.is_authenticated:
        login(request, User.objects.get(username="admin"), 'django.contrib.auth.backends.ModelBackend')

    return redirect(settings.LOGIN_REDIRECT_URL if request.user.is_authenticated
                    else settings.LOGIN_URL)

@login_required
def dashboard(request):
    no_processingnodes = ProcessingNode.objects.count() == 0
    if no_processingnodes and settings.PROCESSING_NODES_ONBOARDING is not None:
        return redirect(settings.PROCESSING_NODES_ONBOARDING)

    no_tasks = Task.objects.filter(project__owner=request.user).count() == 0
    no_projects = Project.objects.filter(owner=request.user).count() == 0

    # Create first project automatically
    if no_projects and request.user.has_perm('app.add_project'):
        Project.objects.create(owner=request.user, name=_("First Project"))

    return render(request, 'app/dashboard.html', {'title': _('Dashboard'),
        'no_processingnodes': no_processingnodes,
        'no_tasks': no_tasks
    })

@login_required
def tpfm_dashboard(request):
    if request.method == 'POST' and request.FILES['fluid_model']:
        fluid_model_file = request.FILES['fluid_model']
        # Define the directory where you want to save the file within MEDIA_ROOT
        upload_directory = 'fluid_models'
        # Construct the absolute path to the upload directory
        upload_path = os.path.join(settings.MEDIA_ROOT, upload_directory)
        # Create the directory if it doesn't exist
        os.makedirs(upload_path, exist_ok=True)
        # Construct the absolute file path
        file_path = os.path.join(upload_path, fluid_model_file.name)
        # Handle the uploaded file, for example, save it to the server
        # (You may need to adjust the path to where you want to save the file)
        with open(file_path, 'wb+') as destination:
            for chunk in fluid_model_file.chunks():
                destination.write(chunk)
        # Optionally, you can redirect the user to another page after the upload
        return render(request, 'app/tpfm/tpfm_dashboard.html', {'upload_success': True})
    return render(request, 'app/tpfm/tpfm_dashboard.html', {'title': _('Turbine planner & Fluid modelling'),'upload_success': False})


@login_required
def export_to_csv(request, hydrosurvey_pk=None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hydrosurvey.csv"'

    writer = csv.writer(response)
    hydrosurvey_fields = ['deadline', 'status', 'water_surface', 'location', 'flow_direction', 'flow_direction_speed', 'segment_width', 'segment_depth', 'estimated_waterflow', 'estimated_energy_production']
    
    writer.writerow(hydrosurvey_fields)
      
    if hydrosurvey_pk:
        survey_all = list(vars(get_object_or_404(HydroSurvey, pk=hydrosurvey_pk)).values())[2:]
        print(list(survey_all))
    
    # Assuming the HydroSurvey model has its fields in the same order as the hydrosurvey_fields variable
    writer.writerow(survey_all)
        
    return response

@login_required
def export_project_to_csv(request, project_id=None):
    response = HttpResponse(content_type='text/csv')
    # TODO: let the user decide the filename
    response['Content-Disposition'] = 'attachment; filename="project.csv"'

    writer = csv.writer(response)
    project_fields = ['name', 'created_at', 'project_status_id', 'deadline', 'team_id', 'description', 'report_id']
    
    writer.writerow(project_fields)

    if project_id:
        hydroproject = get_object_or_404(HydroProject, pk=project_id)
        
        csv_list = []
        
        for field in project_fields:
            if field in vars(hydroproject):
                csv_list.append(vars(hydroproject).get(field))
        
    
    # Assuming the HydroProject model has its fields in the same order as the project_fields variable
    writer.writerow(csv_list)
        
    return response

@login_required
def hydro_survey(request, hydrosurvey_pk=None):
    form = HydroSurveyForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            
            survey = form.save()
            
            return redirect('data_collection')
    else:
        form = HydroSurveyForm()
        
    if hydrosurvey_pk:
        survey = get_object_or_404(HydroSurvey, pk=hydrosurvey_pk)
        return render(request, 'app/psm/data_collection.html', {'survey': survey}, {'form': form})
    
    return render(request, 'app/psm/data_collection.html', {'form': form})

@login_required
def hydro_survey_list(request):
    
    hydrosurveys = HydroSurvey.objects.all()
    
    
    return render(request, 'app/psm/data_collection.html', {'hydrosurveys': hydrosurveys}) 


@login_required
def flow_simulation(request):  
    return render(request, 'app/tpfm/flow_simulation.html', {'title': _('Flow Simulation')})

@login_required
def pressure_analysis(request):
    return render(request, 'app/tpfm/pressure_analysis.html', {'title': _('Pressure Analysis')})

@login_required
def turbine_efficiency_modelling(request):
    return render(request, 'app/tpfm/turbine_efficiency_modelling.html', {'title': _('Turbine Efficiency Modelling')})

@login_required
def threed_modelling(request):
    return render(request, 'app/tpfm/3d_model_turbine.html', {'title': _('ThreeD Modelling'), 'version': settings.VERSION})

@login_required
def planning_scenario_modelling(request):
    return render(request, 'app/psm/psm_dashboard.html', {'title': _('Planning scenario modelling')})

@login_required
def report(request, report_id=None):
    if report_id:
        report = Report.objects.get(id=report_id)
        tasks,completion_ratios = report.tasks_completion()
        print(tasks)
        print(completion_ratios)
                # Create a bar plot
        plt.figure(figsize=(8, 6))
        plt.bar(tasks, completion_ratios, color='skyblue')

        # Adding labels and title
        plt.xlabel('Tasks')
        plt.ylabel('Completion Ratio')
        plt.title('Task Completion Ratio')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.getvalue()).decode()
        html = f'<img src="data:image/png;base64,{plot_data}" alt="Task Completion Ratio">'
# Encode the BytesIO object to base64
       
        return render(request, 'app/psm/project_planning.html', {'title': _('Project Planning'), 'report':report, 'html': html}) #, 'tasks_status': tasks_status
    reports = Report.objects.order_by('project')
    return render(request, 'app/psm/project_planning.html', {'title': _('Project Planning'), 'reports':reports})
    
@login_required
def project_planning(request, project_id=None):
    projects = HydroProject.objects.all()
    if project_id is not None:
        project = HydroProject.objects.get(pk=project_id)
        statuses = ProjectStatus.objects.all()
        tasks = HydroTask.objects.filter(project=project.id)
        task_statuses = TaskStatus.objects.all()
        team_id = project.team
        team_members = TeamMember.objects.filter(team = team_id)
        project_reports = Report.objects.filter(project=project_id)
        if request.method == "POST":
            task_name = request.POST.get('task_name')
            task_deadline = request.POST.get('task_deadline')
            task_status = request.POST.get('task_status')
            task_description = request.POST.get('task_description')
            project_id = request.POST.get('project_id')
            task_start_date = request.POST.get('task_start_date')
            task_color = request.POST.get('task_color')
            if task_name:
                task = HydroTask.objects.create(
                    name=task_name,
                    deadline = task_deadline,
                    status_id = task_status,
                    description = task_description,
                    project_id = project_id,
                    start_date = task_start_date,
                    color = task_color
                )
            return render(request, 'app/psm/project_planning.html', {'title': _('Project Planning'), 'project':project, 'statuses':statuses, 'tasks':tasks, 'task_statuses': task_statuses, 'team_members':team_members, 'project_reports':project_reports, 'add_new_task': True})
        elif request.method == "GET":
            return render(request, 'app/psm/project_planning.html', {'title': _('Project Planning'), 'project':project, 'statuses':statuses, 'tasks':tasks, 'task_statuses': task_statuses, 'team_members':team_members, 'project_reports':project_reports, 'add_new_task': False})
    return render(request, 'app/psm/project_planning.html', {'title': _('Project Planning'), 'projects':projects})

@login_required
def calendar_view(request, project_id=None):
    if project_id == None:
        return redirect('app/psm/fullcalendar.html')
    project = get_object_or_404(HydroProject, pk=int(project_id))
    tasks = HydroTask.objects.filter(project=project.id)
    return render(request, 'app/psm/fullcalendar.html', {'tasks':tasks})

@login_required
def delete_project(request, project_id):
    projects = HydroProject.objects.all()
    if request.method == "POST":
        HydroProject.objects.filter(id=project_id).delete()
        return render(request, 'app/psm/project_planning.html', {'title': _('Project Planning'), 'projects':projects})
    
@login_required
def save_project(request, project_id):   
    if project_id is not None and request.method == "POST":
        project = HydroProject.objects.get(id=project_id)
        statuses = ProjectStatus.objects.all()
        tasks = HydroTask.objects.filter(project=project_id)
        task_statuses = TaskStatus.objects.all()
        team_id = project.team
        team_members = TeamMember.objects.filter(team = team_id)
        status = ProjectStatus.objects.get(id = request.POST.get('project_status'))
        project.project_status = status
        project.deadline = request.POST.get('project_deadline')
        project.save()
        project = HydroProject.objects.get(id=project_id)    
    return render(request, 'app/psm/project_planning.html', {'title': _('Project Planning'), 'project':project, 'statuses':statuses, 'tasks':tasks, 'task_statuses': task_statuses, 'team_members':team_members,'add_new_task': False})

@login_required
def add_project(request):
    statuses = ProjectStatus.objects.all()
    teams = Team.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status_id')
        status = ProjectStatus.objects.get(id=status)
        deadline = request.POST.get('deadline')
        team = request.POST.get('team_id')
        team = Team.objects.get(id = team)
        project = HydroProject.objects.create(name = name,
                                              created_at = datetime.date.today().strftime("%Y-%m-%d"),
                                              description = description,
                                              project_status = status,
                                              deadline = deadline,
                                              team =  team)
    return render(request, 'app/psm/add_project.html', {'title': _('Project Planning'), 'statuses':statuses, 'teams':teams})

@login_required
def statistics(request):
    return render(request, 'app/psm/project_planning.html', {'title': _('Project statistics')}) 

@login_required
def data_collection(request):
    return render(request, 'app/psm/data_collection.html', {'title': _('Data Collection')})

# def turbine_planner(request):
#     return render(request, 'app/templates/app/public/3d_model_turbine.html', {'title': _('Turbine and waterflow planner'), 'version': settings.VERSION})

@login_required
def map(request, project_pk=None, task_pk=None):
    title = _("Map")

    if project_pk is not None:
        project = get_object_or_404(Project, pk=project_pk)
        if not request.user.has_perm('app.view_project', project):
            raise Http404()
        
        if task_pk is not None:
            task = get_object_or_404(Task.objects.defer('orthophoto_extent', 'dsm_extent', 'dtm_extent'), pk=task_pk, project=project)
            title = task.name or task.id
            mapItems = [task.get_map_items()]
        else:
            title = project.name or project.id
            mapItems = project.get_map_items()

    return render(request, 'app/map.html', {
            'title': title,
            'params': {
                'map-items': json.dumps(mapItems),
                'title': title,
                'public': 'false',
                'share-buttons': 'false' if settings.DESKTOP_MODE else 'true'
            }.items()
        })

@login_required
def model_display(request, project_pk=None, task_pk=None):
    title = _("3D Model Display")

    if project_pk is not None:
        project = get_object_or_404(Project, pk=project_pk)
        if not request.user.has_perm('app.view_project', project):
            raise Http404()

        if task_pk is not None:
            task = get_object_or_404(Task.objects.defer('orthophoto_extent', 'dsm_extent', 'dtm_extent'), pk=task_pk, project=project)
            title = task.name or task.id
        else:
            raise Http404()

    return render(request, 'app/3d_model_display.html', {
            'title': title,
            'params': {
                'task': json.dumps(task.get_model_display_params()),
                'public': 'false',
                'share-buttons': 'false' if settings.DESKTOP_MODE else 'true'
            }.items()
        })

def about(request):
    return render(request, 'app/about.html', {'title': _('About'), 'version': settings.VERSION})
    
@login_required
def processing_node(request, processing_node_id):
    pn = get_object_or_404(ProcessingNode, pk=processing_node_id)
    if not pn.update_node_info():
        messages.add_message(request, messages.constants.WARNING, _('%(node)s seems to be offline.') % {'node': pn})

    return render(request, 'app/processing_node.html', 
            {
                'title': _('Processing Node'), 
                'processing_node': pn,
                'available_options_json': pn.get_available_options_json(pretty=True)
            })

class FirstUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', )
        widgets = {
            'password': forms.PasswordInput(),
        }


def welcome(request):
    if User.objects.filter(is_superuser=True).count() > 0:
        return redirect('index')

    fuf = FirstUserForm()

    if request.method == 'POST':
        fuf = FirstUserForm(request.POST)
        if fuf.is_valid():
            admin_user = fuf.save(commit=False)
            admin_user.password = make_password(fuf.cleaned_data['password'])
            admin_user.is_superuser = admin_user.is_staff = True
            admin_user.save()

            # Log-in automatically
            login(request, admin_user, 'django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')

    return render(request, 'app/welcome.html',
                  {
                      'title': _('Welcome'),
                      'firstuserform': fuf
                  })


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
