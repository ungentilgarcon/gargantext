
from django.shortcuts import redirect

from django.shortcuts import render

import datetime

from django.http import Http404, HttpResponse
from django.template.loader import get_template
from django.template import Context

from documents.models import Project, Corpus, Document

from itertools import *
from django.db import connection

def query_to_dicts(query_string, *query_args):
    """Run a simple query and produce a generator
    that returns the results as a bunch of dictionaries
    with keys for the column values selected.
    """
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(zip(col_names, row))
        yield row_dict
    return

def home(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    
    t = get_template('home.html')

    date = datetime.datetime.now()
    projects = Project.objects.all().order_by("-date")
    number = len(projects)

    html = t.render(Context({\
            'date': date,\
            'projects': projects,\
            'number': number,\
            }))
    
    return HttpResponse(html)


def project(request, p_id):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    
    try:
        offset = str(p_id)
    except ValueError:
        raise Http404()

    t = get_template('project.html')

    date = datetime.datetime.now()
    project = Project.objects.get(pk=p_id)
    corpora = Corpus.objects.all().filter(project_id=p_id)
    number = len(corpora)
    
    html = t.render(Context({\
            'date': date,\
            'project': project,\
            'corpora' : corpora,\
            'number': number,\
            }))
    
    return HttpResponse(html)


def corpus(request, p_id, c_id):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    
    try:
        offset = str(p_id)
    except ValueError:
        raise Http404()

    t = get_template('corpus.html')

    date = datetime.datetime.now()
    project = Project.objects.get(pk=p_id)
    corpus  = Corpus.objects.get(pk=c_id)
    documents  = Document.objects.all().filter(corpus_id=c_id).order_by("-date")
    number = len(documents)

    sources = query_to_dicts('''select count(*),source 
                        from documents_document
                        where corpus_id = %d
                        group by source
                        order by 1 DESC limit %d;''' % (int(c_id), int(15)))

    
    dates = query_to_dicts('''select to_char(date, 'YYYY'), count(*) 
                            from documents_document 
                            where corpus_id = %d
                            group by to_char(date, 'YYYY')
                            order by 1 DESC;''' %  (int(c_id),))
    
    
    html = t.render(Context({\
            'date': date,\
            'project': project,\
            'corpus' : corpus,\
            'documents': documents,\
            'number' : number,\
            'sources' : sources,\
            'dates' : dates,\
            }))
    
    return HttpResponse(html)

