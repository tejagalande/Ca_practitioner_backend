from django.urls import path
from ca_app.views import *

urlpatterns = [
    path('gstNoticeOrder/', gstNoticeOrder, name='gstNoticeOrder'),
    path('gstSorNotice/', gst_sor_notice, name='gst_sor_notice'),
    path('clientInfo/', client_info, name='client_info'),
    path('uploadFile/', upload_file, name='upload_file'),
    path('viewFile/', view_file, name='view_file'),
    path('downloadFile/', download_file, name='download_file'),
    path('status/', notice_status, name='notice_status'),
    path('notice/', notice, name='notice'),
    path('history/', history, name='history'),
    path('clients/', clients, name='clients'),
    path('reminder/', reminder, name='reminder'),

    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('google/callback/', GoogleCallback.as_view(), name='google_callback'),
    path('add-event/', AddEvent.as_view(), name='add_event'),

    path('getCred/', get_credentials, name='get_credentials'),
   
]
