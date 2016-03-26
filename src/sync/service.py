"""
Service for synchronization
"""
from inventory.utils import file_to_blob
from sync.serializers import ProductDeserializer, ProductSerializer


def sync_products_from_file(input_file):
	try:
		blob = file_to_blob(input_file)
	except IOError:
		print('cannot open file', input_file)

	else:
		counter = 0
		data = ProductDeserializer.parse(blob)
		if data:
			for row in data:
				serializer = ProductSerializer(data=row)
				if serializer.is_valid():
					serializer.validated_data
					serializer.save()
					counter += 1
					print('save product', row)

				else:
					print('not valid parsing data', row)

		return counter
