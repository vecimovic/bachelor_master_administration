# bachelor_master_administration

Kako bi projekt radio potrebno je instalirati:

python=3.7

django

	pip install django

djangosaml2

	pip install djangosaml2

mockdjangosaml2

	pip install mockdjangosaml2

 xhtml2pdf
 
	pip install xhtml2pdf

xmlsec1: http://www.aleksey.com/xmlsec/
 
### Promjene koje je potrebno izvršiti

Dodati folder pod nazivom "media" u glavni direktorij projekta 

#### djangosaml2


##### /home/valentina/anaconda3/envs/env_name/lib/python3.7/site-packages/djangosaml2/backends.py 

linija 119: Promijeniti 

    if not self.is_authorized(attributes, attribute_mapping, idp_entityid):
 
 u
 
    if not self.is_authorized(attributes, attribute_mapping):
    
#### mockdjangosaml2

##### /home/valentina/anaconda3/envs/env_name/lib/python3.7/site-packages/mockdjangosaml2/urls.py 

Promijeniti

		from django.conf.urls import patterns, url

		urlpatterns = patterns(
			'mockdjangosaml2.views',
			url(r'^login/$', 'login', name='saml2_login'),
			url(r'^acs/$', 'assertion_consumer_service', name='saml2_acs'),
			url(r'^logout/$', 'logout', name='saml2_logout'),
		)

u

		from django.urls import path

		from . import views

		urlpatterns = [

		    path('login/', views.login, name='saml2_login'),
		    path('acs/', views.assertion_consumer_service, name='saml2_acs'),
		    path('logout/', views.logout, name='saml2_logout'),
		]

	
##### /home/valentina/anaconda3/envs/env_name/lib/python3.7/site-packages/mockdjangosaml2/views.py 
	
linija 8 : Promijeniti

		from django.contrib.auth.views import logout as django_logout
u

		from django.contrib.auth import logout as django_logout
	
linija 11 : Promijeniti

		from django.shortcuts import render_to_response
u

		from django.shortcuts import render
    
linija 20 : Promijeniti

		from django.core.urlresolvers import reverse
u

    from django.urls import reverse
    
linija 54 : Promijeniti

		if not request.user.is_anonymous()
u

		if not request.user.is_anonymous

linija 135 : Promijeniti

		return django_logout(request, next_page=next_page)
u

      django_logout(request)
      return HttpResponseRedirect(next_page)

ispod linije 106( session_info = request.session['mock_session_info']):  Dodati

    session_info.update( {'issuer' : 'riteh'} )

##### /home/valentina/anaconda3/envs/env_name/lib/python3.7/site-packages/mockdjangosaml2/settings.py

Dodati:

    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_URL = '/static/'
	  STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

##### /home/valentina/anaconda3/envs/env_name/lib/python3.7/site-packages/mockdjangosaml2/templates/mockdjangosaml2/login.html
 
 Dodati:
 
    {% load static %}

 Promijeniti:
 
    <link rel="stylesheet" href="{{ STATIC_URL }}mockdjangosaml2/login.css">
 u
 
    <link rel="stylesheet" href=" {% static "mockdjangosaml2/login.css" %}">

  Promijeniti:
  
	<img class="aai_logo" src="{{ STATIC_URL }}mockdjangosaml2/aai_logo_localhost.png" alt="AAI@localhost logo">
u
  
    <img class="aai_logo" src="{% static "mockdjangosaml2/aai_logo_localhost.png" %}" alt="AAI@localhost logo">
	


