from django.forms import modelformset_factory


class FormSetFactory:

    def __init__(self, data, model, prefix, form, files=None, queryset=None, min_num=None, max_num=None,
                 validate_min=False, validate_max=False, can_delete=False, extra=1, form_kwargs=None):
        self.data = data
        self.model = model
        self.prefix = prefix
        self.form = form
        self.files = files
        self.min_num = min_num
        self.max_num = max_num
        self.validate_min = validate_min
        self.validate_max = validate_max
        self.can_delete = can_delete
        self.form_kwargs = form_kwargs
        self.extra = extra
        self.queryset = queryset
        if queryset and queryset.exists():
            self.extra = 0
        if not queryset:
            self.queryset = self.model.objects.none()

    def get_formset(self):
        formset = modelformset_factory(
            self.model,
            form=self.form,
            extra=self.extra,
            min_num=self.min_num,
            max_num=self.max_num,
            validate_min=self.validate_min,
            validate_max=self.validate_max,
            can_delete=self.can_delete,
        )
        return formset(
            self.data,
            files=self.files,
            prefix=self.prefix,
            queryset=self.queryset,
            form_kwargs=self.form_kwargs
        )
