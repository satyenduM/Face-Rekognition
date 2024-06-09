from celery import Celery
from lambda_functions import call_lambda_function
import os
celery_app = Celery('tasks', broker=os.environ.get('REDIS_URL'), backend=os.environ.get('REDIS_URL'))

@celery_app.task
def process_images(folder_id, reference_image_id):
    
    s3_bucket = call_lambda_function('driveToS3', {'folder_id': folder_id, 'bucket_name': 'face-rekognition2'})
   
   # Call the face_rekog_adv lambda function
    result_bucket = call_lambda_function('face_rekog_adv', {'source_bucket': 'face-rekognition2', 'source_image': reference_image_id, 'target_bucket': 'resultbucket0'})
   
   # Call the zipS3Bucket lambda function
    download_url = call_lambda_function('zipS3Bucket', {'s3_bucket_name': 'resultbucket0'})
   
    return download_url