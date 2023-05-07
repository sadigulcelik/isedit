import ipywidgets as widgets
from traitlets import Unicode
from traitlets import List
from ._version import NPM_PACKAGE_RANGE


@widgets.register
class Ipyscore(widgets.DOMWidget):
    """An  widget."""

    # Name of the widget view class in front-end
    _view_name = Unicode('IpyscoreView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('IpyscoreModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('isedit').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('isedit').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode(NPM_PACKAGE_RANGE).tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(NPM_PACKAGE_RANGE).tag(sync=True)

    # Widget specific property.
    # Widget properties are defined as traitlets. Any property tagged with `sync=True`
    # is automatically synced to the frontend *any* time it changes in Python.
    # It is synced back to Python from the frontend *any* time the model is touched.
    value = List(['text']).tag(sync=True)
    nkeys = List([["cn/4"]]).tag(sync=True)
    durations = List([["q"]]).tag(sync=True)
