import pprint
import boto3
import os

# Many thanks to birryree
# https://stackoverflow.com/questions/41388926/an-example-of-calling-aws-rekognition-http-api-from-python

# This is minimum threshold for similarity
SIMILARITY_THRESHOLD = 75.0

if __name__ == '__main__':
    client = boto3.client('rekognition',
                          aws_access_key_id='AKIAIN6PFQ6HXSVVFUWA',
                          aws_secret_access_key='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',
                          )
    # TODO: Change image file paths to no longer be local
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
    with open('./joanna0.jpg', 'rb') as image:
        labelsData = client.detect_labels(Image={'Bytes': image.read()})

    # SINGLE IMAGE VECTORS
    with open('./joanna0.jpg', 'rb') as image:
        facesData = client.detect_faces(Image={'Bytes': image.read()})

    print('Detected labels in labels data: ')
    for i in labelsData['Labels']:
        print(i['Name'] + ' : ' + str(i['Confidence']))
    # pprint.pprint(labelsData)

    print('Detected labels in faces data: ')
    #for i in facesData['FaceDetails']:
    #    print(facesData[0][i])
    pprint.pprint(facesData)
