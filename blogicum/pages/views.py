from django.views.generic import TemplateView

from django.shortcuts import render


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class RulesPageView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    context = {'exception': exception}
    return render(request, 'pages/404.html', context, status=404)


def csrf_failure(request, reason=''):
    context = {'reason': reason}
    return render(request, 'pages/403csrf.html', context, status=403)


def server_error(request, reason=''):
    context = {'reason': reason}
    return render(request, 'pages/500.html', context, status=500)
