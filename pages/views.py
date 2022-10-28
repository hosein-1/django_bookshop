from django.views import generic


class AboutUsPageView(generic.TemplateView):
    template_name = 'pages/about_us.html'
