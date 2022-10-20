from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
# using 'as _' means we can call gettext_lazy using _() it acts like an alias


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'