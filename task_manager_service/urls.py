from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("tasks/", include("task_manager.urls", namespace="task-manager"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
