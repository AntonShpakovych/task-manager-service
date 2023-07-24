from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


handler404 = 'task_manager_service.views.handler_404'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", RedirectView.as_view(url="tasks/", permanent=True)),
    path("tasks/", include("task.urls", namespace="task")),
    path("employees/", include("employee.urls", namespace="employee"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
