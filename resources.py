import boto3, string, random, os
from flask import session

S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY = os.getenv('S3_KEY')
S3_SECRET = os.getenv('S3_SECRET')

def _get_s3_resource():
    if S3_KEY and S3_SECRET:
        return boto3.resource(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.resource('s3')

def get_bucket():
    s3_resource = _get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    else:
        bucket = S3_BUCKET

    return s3_resource.Bucket(bucket)


def generate_key_string():
    tokens = string.ascii_uppercase + string.ascii_lowercase + string.digits  # quais caracteres aceitos
    segmentos_char = 5  # numero de caracteres por segmento
    segmentos = 4  # numero de segmentos
    key_string = ''  # chave a ser gerada

    for x in range(segmentos):
        key_string += ''.join(random.choice(tokens) for y in range(segmentos_char))
    return key_string
