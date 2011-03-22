from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_restapi.responder import *
from django_restapi.receiver import *
from schools.models import *

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm
from fullhistory.models import FullHistory
from django.db.models import Q
import datetime

def KLP_audit(request):
    user = request.user     
    check_user_perm.send(sender=None, user=user, model='Audit', operation=None)
    check_user_perm.connect(KLP_user_Perm)
    userList = User.objects.filter(is_active=1)
    respDict = {'userList':userList, 'title':'Karanataka Learning Partnership'}
    if request.POST:
    	selUser = request.POST.get('selUser')
    	defaultDate = datetime.date.today().strftime("%d")+'-'+datetime.date.today().strftime("%m")+'-'+datetime.date.today().strftime("%Y")
    	startDate = request.POST.get('startDate')
    	endDate = request.POST.get('endDate')
    	if not startDate:
    		startDate = defaultDate
    	if not endDate:
    		endDate = defaultDate
    	respDict['startDate'] = startDate
    	respDict['endDate'] = endDate
    	respDict['selUser'] = int(selUser)
    	strDate = startDate.split('-')
    	enDate = endDate.split('-')
    	fullHistoryList = FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=selUser)
    	respDict['fullHistoryList'] = fullHistoryList
    	return render_to_response('viewtemplates/auditTrial.html',respDict,context_instance=RequestContext(request)) 
    return render_to_response('viewtemplates/auditTrial.html',respDict,context_instance=RequestContext(request)) 
        
 
    
    
urlpatterns = patterns('',           
   url(r'^audit/trial/$', KLP_audit),
)    