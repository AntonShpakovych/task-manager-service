from django.urls import path

from employee.views import (
    EmployeeListView,
    EmployeeDeleteView,
    EmployeeUpdateView,
    EmployeeDetailView,
    EmployeeCreateView,
    PositionListView,
    PositionDetailView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView
)


urlpatterns = [
    path(
        "",
        EmployeeListView.as_view(),
        name="employee-list"
    ),
    path(
        "create/",
        EmployeeCreateView.as_view(),
        name="employee-create"
    ),
    path(
        "<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete"
    ),
    path(
        "<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee-update"
    ),
    path(
        "<int:pk>/detail/",
        EmployeeDetailView.as_view(),
        name="employee-detail"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/<int:pk>/detail/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
]

app_name = "employee"
