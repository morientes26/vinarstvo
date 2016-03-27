from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sync.serializers import ProductSerializer
from inventory.models import Product


class SyncView(generics.ListAPIView):
	"""
	Returns a list of synchronized data.

	"""
	model = Product
	serializer_class = ProductSerializer

	def get_queryset(self):
		return self.__mock_queryset()

	@staticmethod
	def __mock_queryset():
		"""
		Getting only mocked data for testing sync
		Returns: list of Product

		"""
		return Product.objects.filter(is_new=True)


@api_view(['GET', 'POST'])
def product_sync(request):
	"""
	Getting all product from server.
	"""

	if request.method == 'GET':
		products = Product.objects.filter(is_new=True)
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)