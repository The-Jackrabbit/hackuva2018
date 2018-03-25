import pprint
import boto3
import os
import sys
# Many thanks to birryree
# https://stackoverflow.com/questions/41388926/an-example-of-calling-aws-rekognition-http-api-from-python

# This is minimum threshold for similarity

SIMILARITY_THRESHOLD = 75.0

client = boto3.client('rekognition',
	aws_access_key_id='AKIAJX5ZEY6HMU3CLUMQ',
	aws_secret_access_key='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',
	region_name='us-east-1'
)

# TODO: Change image file paths from local
dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

# TODO: Change from single image to .zip or otherwise a collection
# TODO: Change from comparison between images to straight request that's LINKED to S3 batch

"""
# DUAL IMMAGE COMPARISON

# SOURCE IMAGE
with open('./joanna0.jpg', 'rb') as source_image:
	source_bytes = source_image.read()

# TARGET IMAGE
with open('./joanna1.jpg', 'rb') as target_image:
	target_bytes = target_image.read()


response = client.compare_faces(
	SourceImage = { 'Bytes': source_bytes },
	TargetImage = { 'Bytes': target_bytes },
	SimilarityThreshold = SIMILARITY_THRESHOLD
)
"""

# SINGLE IMAGE VECTORS
with open('./public/ddd.jpg', 'rb') as image:
	labelsData = client.detect_labels(Image={'Bytes': image.read()})

# SINGLE IMAGE VECTORS
with open('./public/ddd.jpg', 'rb') as image:
	facesData = client.detect_faces(Image={'Bytes': image.read()})

json = ""

json +=  'Detected labels in labels data: '
labs = {}
for i in labelsData['Labels']:
	labs[i['Name']] = str(i['Confidence'])
# pprint.pprint(labelsData)
faces = {}
json +=  'Detected labels in faces data: '
#for i in facesData['FaceDetails']:
#    print(facesData[0][i])
faces = facesData

json = {
	'faces': faces,
	'labels': labs
}

print(str(json))
sys.stdout.flush()