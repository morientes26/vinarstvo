from vanilla import TemplateView


class CartView(TemplateView):
    template_name = 'cart/index.html'

    def get(self, request, *args, **kwargs):
        return super(CartView, self).get(request, args, kwargs)