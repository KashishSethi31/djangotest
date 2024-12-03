from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('busdash/', TemplateView.as_view(template_name="bus_template.html"), name='bus'),
    # Add another namespace if needed
    # path('app2_plotly_dash/', include(('django_plotly_dash.urls', 'app2_plotly_dash'), namespace='app2_plotly_dash')),
]

