# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
from django.core import serializers
from .models import Vulnerability, Perimeter, URL, Account, Video
from functools import wraps
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
import tempfile
from .utils import render_to_pdf
from django.views.generic import View
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist

def check_perimeter(function):
  @wraps(function)
  def wrap(request, perimetre_id, *args, **kwargs):
        perimetre = get_object_or_404(Perimeter, id=perimetre_id)
        if request.user.has_perm('view_perimeter', perimetre):
             return function(request, perimetre_id, *args, **kwargs)
        else:
            return redirect('dashboard')
  return wrap

@login_required
def set_permission(request):
    if not request.user.has_perm('change_permission') or not request.user.has_perm('add_permission'):
        return redirect('management')
    return render(request, 'frontend/management.html', {
        'management': request.user.has_perm('view_permission'),
        'success': True
        })

@login_required
def management(request):
    if not request.user.has_perm('view_permission'):
        return redirect('dashboard')
    return render(request, 'frontend/management.html', {
        'management': request.user.has_perm('view_permission')
        })

@login_required
def dashboard(request):
    # TODO: bad logic
    filter_value = request.GET.get('filter')
    perimeters = get_objects_for_user(request.user, 'frontend.view_perimeter')
    per=serializers.serialize("json", perimeters , fields=  ('name','major','minor','moderate'))
    vuln= Vulnerability.objects.all()
    data = serializers.serialize("json", vuln, fields=  ('name','theme','criticality'))
    datas = '<script src="/static/data/dashboard-barData.js" type="text/javascript"></script>'
  #  datas +='<script src="/static/data/dashboard-pieData.js" type="text/javascript"></script>'

    if 'filter' in request.GET:
        perimeters = perimeters.filter(perimeter=request.GET.get('filter'))
        datas = '<script src="/static/data/dashboard-filtered-barData.js" type="text/javascript"></script>'
        datas += '<script src="/static/data/dashboard-filtered-pieData.js" type="text/javascript"></script>'

    perimeters = perimeters.order_by('id')

    return render(request, 'frontend/dashboard.html', {
        'management': request.user.has_perm('view_permission'),
        'perimeters': perimeters,
        'filter': filter_value,
        'datas': datas,
        'vuln' : data,
        'per'  : per,
    })

@login_required
@check_perimeter
def view_perimetre(request, perimetre_id):
    perimetre = get_object_or_404(Perimeter, id=perimetre_id)
    urls = URL.objects.all().filter(perimeter=perimetre)
    accounts = Account.objects.all().filter(perimeter=perimetre)
    vulnerabilities = Vulnerability.objects.all().filter(perimeter=perimetre)
    data = serializers.serialize("json", vulnerabilities, fields=  ('name','theme','criticality'))
    return render(request, 'frontend/perimetre.html', {
        'management': request.user.has_perm('view_permission'),
        'perimetre': perimetre,
        'urls': urls,
        'accounts': accounts,
        'vulnerabilities': vulnerabilities,
        'vuln' : data,
    })

@login_required
def edit_perimetre(request, perimetre_id):
    perimetre = get_object_or_404(Perimeter, id=perimetre_id)
    if not request.user.has_perm('change_perimeter', perimetre):
        return redirect('dashboard')
    return render(request, 'frontend/perimetre.html', {
        'management': request.user.has_perm('view_permission'),
        'perimetre': perimetre_id
    })

@login_required
def create_perimetre(request):
    if not request.user.has_perm('add_perimeter'):
        return redirect('dashboard')
    return render(request, 'frontend/perimetre.html', {
        'management': request.user.has_perm('view_permission')
     })

@login_required
@check_perimeter
def view_vulnerability(request, perimetre_id, vulnerability_id):
    perimetre = get_object_or_404(Perimeter, id=perimetre_id)
    vuln = get_object_or_404(Vulnerability, id=vulnerability_id)
   # data = serializers.serialize("json", vuln, fields=('vector', 'complexity', 'interaction', 'privileges','scope','availability','integrity','confidentiality'))
    if vuln.perimeter != perimetre:
        return redirect(view_perimetre, perimetre_id)
    try:
        video= Video.objects.get(vulnerability=vuln)
        return render(request, 'frontend/vulnerability.html', {
            'management': request.user.has_perm('view_permission'),
            'perimetre': perimetre,
            'vuln': vuln,
            'video': video,
    #        'data': data ,
        })
    except ObjectDoesNotExist:
        return render(request, 'frontend/vulnerability.html', {
            'management': request.user.has_perm('view_permission'),
            'perimetre': perimetre,
            'vuln': vuln,
     #       'data': data,
            'text' :"Il n' y a pas de vidéo disponible pour cette vulnérabilité"
        })





@login_required
def edit_vulnerability(request, perimetre_id, vulnerability_id):
    perimetre = get_object_or_404(Perimeter, id=perimetre_id)
    vuln = get_object_or_404(Vulnerability, id=vulnerability_id)
    if not request.user.has_perm('view_perimeter', perimetre):
        return redirect('dashboard')
    if not request.user.has_perm('change_vulnerability', perimetre, vuln):
        return redirect('view_perimetre', perimetre_id)
    return render(request, 'frontend/vulnerability.html', {
        'management': request.user.has_perm('view_permission'),
        'perimetre': perimetre,
        'vulnerability': vuln
    })

@login_required
def create_vulnerability(request, perimetre_id):
    perimetre = get_object_or_404(Perimeter, id=perimetre_id)
    if not request.user.has_perm('view_perimeter', perimetre):
        return redirect('dashboard')
    if not request.user.has_perm('add_vulnerability', perimetre):
        return redirect('view_perimetre', perimetre_id)
    return render(request, 'frontend/vulnerability.html', {
        'management': request.user.has_perm('view_permission'),
        'perimetre': perimetre
    })
@login_required
def html_to_pdf_view(request,perimetre_id):
    perimetre = get_object_or_404(Perimeter, id=perimetre_id)
    urls = URL.objects.all().filter(perimeter=perimetre)
    accounts = Account.objects.all().filter(perimeter=perimetre)
    vulnerabilities = Vulnerability.objects.all().filter(perimeter=perimetre)
    html_string = render_to_string('frontend/perimetre.html', {
        'management': request.user.has_perm('view_permission'),
        'perimetre': perimetre,
        'urls': urls,
        'accounts': accounts,
        'vulnerabilities': vulnerabilities
    })
    html = HTML(string=html_string)
    font_config = FontConfiguration()
    result=html.write_pdf(font_config=font_config)

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


class GeneratePDF(View):
    def get(self, request, perimetre_id):
        template = get_template('frontend/perimetre.html')
        perimetre = get_object_or_404(Perimeter, id=perimetre_id)
        urls = URL.objects.all().filter(perimeter=perimetre)
        accounts = Account.objects.all().filter(perimeter=perimetre)
        vulnerabilities = Vulnerability.objects.all().filter(perimeter=perimetre)
        context = {
            'management': request.user.has_perm('view_permission'),
            'perimetre': perimetre,
            'urls': urls,
            'accounts': accounts,
            'vulnerabilities': vulnerabilities
        }
        html = template.render(context)
        pdf = render_to_pdf('frontend/perimetre.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

