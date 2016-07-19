"""
Service for synchronization
"""
from inventory.utils import file_to_blob
from sync.serializers import ProductDeserializer, ProductSerializer
from inventory.models import Product
from django.core.exceptions import ObjectDoesNotExist

#import logging

#logger = logging.getLogger(__name__)

def sync_products_from_file(input_file):
	try:
		blob = file_to_blob(input_file)
		#logger.debug(input_file)
		print(input_file)
	except IOError:
		#logger.error('cannot open file', input_file)
		print('cannot open file', input_file)

	else:
		counter = 0
		data = ProductDeserializer.parse(blob)
		print(data)
		if data:
			for row in data:
				serializer = ProductSerializer(data=row)
				if serializer.is_valid():
					#print('test %s', serializer['code'])
					code = serializer.validated_data['code']
					try:
						product = Product.objects.get(code=code)
						print('update product')
						product.price = serializer.validated_data['price']
						product.amount = serializer.validated_data['amount']
						product.save()
					except ObjectDoesNotExist:
						print('import product', row)
						serializer.save()

					counter += 1
					#logger.debug('import product', row)
					print('import product', row)

				else:
					#logger.error('not valid parsing data %s', row)
					print('not valid parsing data %s', row)

		return counter
