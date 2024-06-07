from celery import Celery
from lambda_functions import call_lambda_function
celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task
def process_images(folder_id, reference_image_id):
    
    s3_bucket = call_lambda_function('driveToS3', {'folder_id': folder_id, 'bucket_name': 'face-rekognition2'})
   
   # Call the face_rekog_adv lambda function
    result_bucket = call_lambda_function('face_rekog_adv', {'source_bucket': 'face-rekognition2', 'source_image': reference_image_id, 'target_bucket': 'resultbucket0'})
   
   # Call the zipS3Bucket lambda function
    download_url = call_lambda_function('zipS3Bucket', {'s3_bucket_name': 'resultbucket0'})
   
    return download_url