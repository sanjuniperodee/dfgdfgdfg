from django.urls import path
from .views import *

urlpatterns = [
    path('user_exists', CheckUserView.as_view(), name='check-user-exists'),
    path('registration-request', RegisterRequestView.as_view(), name='registration-request'),
    path('registration-confirm', RegisterView.as_view(), name='registration-request'),
    path('login', LoginView.as_view(), name='login'),
    path('user', UserView.as_view(), name='get-user-info'),
    path('documents', UserDocuments.as_view(), name='get-user-documents'),
    path('upload_document', UploadDocumentView.as_view(), name='upload-document'),
    path('application', ApplicationView.as_view(), name='get-application'),
    path('approve', ApproveApplicationView.as_view(), name='approve-application'),
]
