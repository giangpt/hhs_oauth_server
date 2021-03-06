#!/usr/bin/env python
from decorate_url import decorated_url
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from apps.accounts.views.oauth2_profile import (openidconnect_userinfo,
                                                userinfo_w_login)
from apps.dot_ext.views.dcrp import register
from apps.fhir.bluebutton.views.home import fhir_conformance
from apps.fhir.bluebutton.views.home import fhir_search_home
from hhs_oauth_server.hhs_oauth_server_context import IsAppInstalled
admin.autodiscover()

ADMIN_REDIRECTOR = getattr(settings, 'ADMIN_PREPEND_URL', '')

urlpatterns = [
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^connect/userinfo', openidconnect_userinfo,
        name='openid_connect_userinfo'),
    url(r'^userinfo', userinfo_w_login,
        name='openid_connect_user_w_login'),
    url(r'^register', register, name='dcrp_register'),
    url(r'.well-known/', include('apps.wellknown.urls')),
    url(r'^consent/', include('apps.fhir.fhir_consent.urls')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^protected/bluebutton/fhir/v1/$',
        fhir_conformance, name='fhir_conformance'),
    url(r'^protected/bluebutton/fhir/v1/metadata',
        fhir_conformance, name='fhir_conformance_metadata'),
    url(r'^protected/bluebutton/fhir/v1/meta',
        fhir_conformance, name='fhir_conformance_meta'),
    url(r'^protected/bluebutton/fhir/v1/',
        include('apps.fhir.bluebutton.urls_oauth')),
    url(r'^bluebutton/fhir/v1/', include('apps.fhir.bluebutton.urls')),
    url(r'^capabilities/', include('apps.capabilities.urls')),
    url(r'^endorsements/', include('apps.dot_ext.endorsementurls')),
    url(r'^home/', include('apps.home.urls')),
    url(r'^o/', include('apps.dot_ext.urls')),
    # Adding Medicare Notices and Warning pages
    url(r'notices',
        TemplateView.as_view(template_name='authorize/notices.html'),
        name='notices'),
    url(r'warnings',
        TemplateView.as_view(template_name='authorize/warnings.html'),
        name='warnings'),

    url(r'^social-auth/', include('social_django.urls', namespace='social')),
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    decorated_url(r'^' + ADMIN_REDIRECTOR + 'admin/', include(admin.site.urls),
                  wrap=staff_member_required(login_url=settings.LOGIN_URL)),
]

if IsAppInstalled("apps.extapi"):
    urlpatterns += [
        url(r'^extapi/', include('apps.extapi.urls')),
    ]

if IsAppInstalled("apps.testclient"):
    urlpatterns += [
        url(r'^testclient/', include('apps.testclient.urls')),
    ]

urlpatterns += [
    # Catch all
    url(r'^$', fhir_search_home, name='home'),
]
