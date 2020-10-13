from django.conf.urls import include, url

import core.views


urlpatterns = [
    # Core views
    url(
        r'^history/(?P<content_type>[0-9]+)/(?P<object_id>[0-9]+)/',
        core.views.ObjectHistoryView.as_view(),
        name='history'
    ),

    # Scan barcodes
    url(r'^scan/', include([
        url(r'^modal/$', core.views.ScannerModalView.as_view(), name='scanner_modal'),
    ])),
]

handler403 = core.views.PermissionErrorView.as_view()
handler404 = core.views.PageNotFoundErrorView.as_view()
handler500 = core.views.ServerErrorView.as_view()
