from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from inventory.serializer import ProductSerializer
from inventory.models import Product
from inventory.service import InventoryService


""" API of inventory modul. It is used by external web application """

class ApiInfoView(APIView):
	"""
	Info about API
	"""

	version = "0.0.1"
	author = "tp-soft s.r.o."	
	renderer_classes = (JSONRenderer, )

	def get(self, request, format=None):
		content = {
			'version': self.version,
			'author': self.author
		}
		return Response(content)


"""
Getting all products from primary winecart
"""
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_from_primary_cart(request):
	products = InventoryService().get_all_products_in_cart()
	serializer = ProductSerializer(products, many=True)
	json = JSONRenderer().render(serializer.data)
	return Response(json)

"""
Getting one product by primary key
"""
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_product_by_id(request, *args, **kwargs):
	product = InventoryService().get_product_by_id(kwargs['pk'])
	serializer = ProductSerializer(product, many=True)
	json = JSONRenderer().render(serializer.data)
	return Response(json)