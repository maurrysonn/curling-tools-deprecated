# -*- coding: utf-8 -*-

# --------------------------
# CHANGE LIST UTILS
# --------------------------

CL_SEARCH_STR = 'q'
CL_ORDERING_STR = 'o'

class ChangeListInfosWrapper(object):
    "Wrapper infos about change list."

    def __init__(self, list_view):
        # Init list_view data
        self.list_view_class = list_view.__class__.__name__
        self.model = list_view.model
        self.list_display = list_view.list_display
        self.list_display_links = list_view.list_display_links
        self.GET_params = list_view.request.GET
        self._prepare_GET_params()
        # Internal data
        self._fields_data = None

    def _prepare_GET_params(self):
        self.search_params = self.GET_params.get(CL_SEARCH_STR, None)
        self.ordering_params = self.GET_params.get(CL_ORDERING_STR, None)

    def _prepare_fields_data(self):
        "Compute infos needed about fields."
        self._fields_data = []
        model_fields_list = self.model._meta.get_all_field_names()
        for field in self.list_display:
            data = {}
            # Classic Model Field
            if field not in model_fields_list:
                # Not in model fields so error
                raise ImproperlyConfigured("View %s Error : Model `%s` hasn't field named `%s`." % (
                        self.list_view_class, self.model.__name__, field))
            # Field Name
            data['attr'] = field
            # Model Field
            model_field = self.model._meta.get_field(field)
            data['field'] = model_field
            # Verbose Name
            data['verbose_name'] = model_field.verbose_name
            # Is link field ?
            data['link'] = field in self.list_display_links
            # Add this field in fields_data
            self._fields_data.append(data)

    @property
    def current_url(self):
        current_url = []
        if self.search_params:
            current_url.append(u'%s=%s' % (CL_SEARCH_STR, self.search_params))
        if self.ordering_params:
            current_url.append(u'%s%s' % (CL_ORDERING_STR, self.ordering_params))
        if current_url:
            return u'?%s' % ( '&'.join(current_url)) 
        return u''

    @property
    def fields_data(self):
        "Return infos about all displayed fields."
        if self._fields_data is None:
            self._prepare_fields_data()
        return self._fields_data

    @property
    def headers(self):
        """
        Return list of the headers informations.
        
        List of dict which contains verbose name header
        and infos about ordering.
        """
        return [ {'verbose_name': col['verbose_name']}
                 for col in self.fields_data]

    def items_for_obj(self, obj):
        "Get all fields infos for a specific object."
        items_fields = []
        for field in self.fields_data:
            items = {}
            # Get attribute of object
            attr = getattr(obj, field['attr'])
            # Check if callable attribute
            if field.get('callable', False):
                attr = attr()
            # Save value
            items['value'] = attr
            # Check if boolean attribute
            items['is_boolean'] = field.get('boolean', False)
            # Check if link fields
            items['link'] = field['link']
            # Add this items to the list
            items_fields.append(items)
        return items_fields
