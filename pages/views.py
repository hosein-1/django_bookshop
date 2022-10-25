from django.views import generic


class HomePageView(generic.TemplateView):
    template_name = 'pages/home.html'


class AboutUsPageView(generic.TemplateView):
    template_name = 'pages/about_us.html'
