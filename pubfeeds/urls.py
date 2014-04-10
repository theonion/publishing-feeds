from django.conf.urls import patterns, include, url

from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pubfeeds.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^onion/4/manifest\.xml', RedirectView.as_view(url="/onion/5/manifest.xml")),
    url(r'', include('pubfeeds.core.urls'))
)
