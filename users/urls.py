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
    path('applications', ApplicationAdminView.as_view(), name='get-all-applications'),
    path('approve', ApproveApplicationView.as_view(), name='approve-application'),
    path('universities/<search>', UniversitiesView.as_view(), name='get-universities'),
    path('university/<slug>', UniversityBySlugView.as_view(), name='university-by-slug'),
    path('user/update/<str:field>/', update_user, name='update_user'),
    path('document/update/<str:id>', EditDocumentStatusView.as_view(), name='edit-document-status')

]
