import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, jsonify, request, redirect

s3_blueprint = Blueprint('s3_blueprint', __name__)

BUCKET_NAME = 'jpadjasek-terraform'
DIR_PREFIX = 'cvs/'


@s3_blueprint.route('/cv', methods=['GET'])
def get_cvs():
    cvs = list_files()
    return jsonify(cvs)


@s3_blueprint.route("/cv", methods=['POST'])
def upload():
    file = request.files['file']
    upload_file(file)
    return redirect("/cv")


def list_files():
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=DIR_PREFIX, StartAfter='cvs/')['Contents']:
        contents.append(item['Key'])

    return contents


def upload_file(user_id, file):
    object_name = file.filename
    s3_client = boto3.client('s3')
    response = s3_client.upload_fileobj(file, BUCKET_NAME, f'{DIR_PREFIX}{user_id}/{object_name}')

    return response


def get_presigned_url(user_id, object_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': BUCKET_NAME,
                                                            'Key': f'{DIR_PREFIX}{user_id}/{object_name}'},
                                                    ExpiresIn=3600)
    except ClientError as e:
        return None
    return response


def delete_user_cv(user_id):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    try:
        bucket.objects.filter(Prefix=f'{DIR_PREFIX}{user_id}/').delete()
    except ClientError as e:
        return None
