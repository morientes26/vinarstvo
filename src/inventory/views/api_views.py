from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from inventory.serializer import ProductSerializer, EventSerializer, OrderSerializer
from inventory.models import Product, Item
from inventory.service import InventoryService

""" API of inventory modul. It is used by external web application """


class ApiInfoView(APIView):
	"""
	Info about API
	"""

	version = "0.0.1"
	author = "tp-soft s.r.o."
	renderer_classes = (JSONRenderer,)

	def get(self):
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
def get_product_from_primary_cart(request):
	print(request.GET.get('group'))
	products = InventoryService().get_all_products_in_cart(request.GET.get('group'))
	serializer = ProductSerializer(products, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


"""
Getting all products from actual event
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_product_from_actual_event(request):
	print(request.GET.get('group'))
	event = InventoryService().get_actual_events(request.GET.get('group'))
	products = None
	if len(event) > 0:
		products = InventoryService().get_all_products_in_event(event[0])
	serializer = ProductSerializer(products, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


"""
Getting all products from actual event
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_actual_event():
	event = InventoryService().get_actual_events('%')
	if event:
		serializer = EventSerializer(event[0], many=False)
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response(None, status=status.HTTP_200_OK)


"""
Getting one product by primary key
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_products(request):
	products = InventoryService().get_products(request.GET.get('group'))
	if products:
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response(None, status=status.HTTP_200_OK)


"""
Getting one product by primary key
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_product_by_id(request, *args, **kwargs):
	product = InventoryService().get_product_by_id(kwargs['pk'])
	print(product)
	serializer = ProductSerializer(product, many=False)
	print(serializer.data)
	return Response(serializer.data, status=status.HTTP_200_OK)


"""
Create order
"""


@api_view(['PUT', 'POST'])
@permission_classes((AllowAny,))
def create_order(request):
	serializer = OrderSerializer(data=request.data)
	print(serializer)
	if serializer.is_valid():
		order = serializer.save()
		# TODO: toto je trocha hack, treba upravit serializer aby nebolo potrebne nastavovat items
		set_items_and_save(request, order)
		# ---------------------------------------------------------------------
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def set_items_and_save(request, order):
	for item in request.data['items']:
		try:
			product = Product.objects.get(pk=item['product'])
			it = Item.objects.create(product=product, amount=item['amount'])
			order.items.add(it)
		except Product.DoesNotExist:
			raise ValueError('product ' + str(item['product']) + ' not found')
	order.save()
