# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
import random
from datetime import datetime

# Create your views here.
def index(request):
    if 'total' not in request.session:
        #request.session['updated'] = False
        request.session['total'] = 0
        request.session['log'] = []
    return render (request, 'gold/index.html')

#helper function to update total & build log entry
def helper(request, earn, where, when):
    request.session['total'] += earn
    log = {'event': "Earned " + str(earn) + " gold from the " + where + "! " + "(" + when + ")", 'class': 'earn'}
    request.session['log'].append(log)
    request.session['updated'] = True
    

def process(request):
    # store event time
    when = datetime.now().strftime( "%x, %X")
    
    # collect appropriate value & location then process w/ helper()
    if request.POST['building'] == 'farm':
        earn = random.randint(10,21)
        where = 'farm'
        helper(request, earn, where, when)
    if request.POST['building'] == 'cave':
        earn = random.randint(5,11)
        where = 'cave'
        helper(request, earn, where, when)
    if request.POST['building'] == 'cave':
        earn = random.randint(2,6)
        where = 'house'
        helper(request, earn, where, when)
    if request.POST['building'] == 'casino' :
        earn = random.randint(1,101) - 50
        where = 'casino'
        helper(request, earn, where, when)
        
        # build log entry for casion case
        if earn < 0:
            log = {'event': "Entered a casino and lost " + str(earn) + " gold... Ouch! (" + when +")", 'class': 'loss' }
            request.session['log'].append(log)
            request.session['updated'] = True
        #prevent break-even case (benefit of the doubt:)
        elif earn == 0:
            earn += 1
            helper(request, earn, where, when)
    
    # return  HttpResponse (request.session['log'])
    return redirect ('/')


