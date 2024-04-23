from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from .views import app as app_views, public as public_views, dev as dev_views
from .plugins.views import app_view_handler, root_url_patterns

from app.boot import boot
from webodm import settings
from app.plugins import sync_plugin_db

# Test cases call boot() independently
# Also don't execute boot with celery workers
if not settings.WORKER_RUNNING and not settings.TESTING:
    boot()

# During testing, boot() is not called (see above)
# but we need to know which plugins are available to mount the proper
# routes via urlpatterns.
if settings.TESTING:
    sync_plugin_db()

urlpatterns = [
    url(r'^$', app_views.index, name='index'),
    url(r'^welcome/$', app_views.welcome, name='welcome'),
    url(r'^dashboard/$', app_views.dashboard, name='dashboard'),
    url(r'^tpfm/$', app_views.tpfm_dashboard, name='tpfm_dashboard'),
    url(r'^tpfm/upload/$', app_views.tpfm_dashboard, name='upload_water_surface_model'),
    url(r'^tpfm/flow_simulation/$', app_views.flow_simulation, name='flow_simulation'),
    url(r'^tpfm/turbine_efficiency_modelling/$', app_views.turbine_efficiency_modelling, name='turbine_efficiency_modelling'),
    url(r'^tpfm/3d_modelling/$', app_views.threed_modelling, name='3d_modelling'),
    url(r'^tpfm/pressure_analysis/$', app_views.pressure_analysis, name='pressure_analysis'),
    url(r'^psm/$', app_views.planning_scenario_modelling, name='planning_scenario_modelling'),
    # url(r'^turbine-planner/$', app_views.turbine_planner, name='turbine_planner'),
    
    url(r'^psm/data_collection/$', app_views.hydro_survey, name='data_collection'),
    
    url(r'^psm/hydrosurvey/(?P<hydrosurvey_pk>[^/.]+)/csv/$', app_views.export_to_csv, name='data_collection'),
    
    url(r'^map/project/(?P<project_pk>[^/.]+)/task/(?P<task_pk>[^/.]+)/$', app_views.map, name='map'),
    url(r'^map/project/(?P<project_pk>[^/.]+)/$', app_views.map, name='map'),
    url(r'^3d/project/(?P<project_pk>[^/.]+)/task/(?P<task_pk>[^/.]+)/$', app_views.model_display, name='model_display'),

    url(r'^public/task/(?P<task_pk>[^/.]+)/map/$', public_views.map, name='public_map'),
    url(r'^public/task/(?P<task_pk>[^/.]+)/iframe/map/$', public_views.map_iframe, name='public_iframe_map'),
    url(r'^public/task/(?P<task_pk>[^/.]+)/3d/$', public_views.model_display, name='public_3d'),
    url(r'^public/task/(?P<task_pk>[^/.]+)/iframe/3d/$', public_views.model_display_iframe, name='public_iframe_3d'),
    url(r'^public/task/(?P<task_pk>[^/.]+)/json/$', public_views.task_json, name='public_json'),

    url(r'^processingnode/([\d]+)/$', app_views.processing_node, name='processing_node'),

    url(r'^api/', include("app.api.urls")),

    url(r'^plugins/(?P<plugin_name>[^/.]+)/(.*)$', app_view_handler),

    url(r'^about/$', app_views.about, name='about'),
    
    url(r'^dev-tools/(?P<action>.*)$', dev_views.dev_tools, name='dev_tools'),

    # TODO: add caching: https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#note-on-performance
    url(r'^jsi18n/', JavaScriptCatalog.as_view(packages=['app']), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + root_url_patterns()

handler404 = app_views.handler404
handler500 = app_views.handler500

