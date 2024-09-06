from django.shortcuts import redirect


class GroupRequiredMixin:
    group_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name=self.group_name).exists():
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
