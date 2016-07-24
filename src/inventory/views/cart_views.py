from vanilla import TemplateView


class CartView(TemplateView):
    template_name = 'cart/index.html'

    def get(self, request, *args, **kwargs):
    	context = self.get_context_data()
    	if 'token' in kwargs:		
        	context['token'] = kwargs['token']
        return self.render_to_response(context)