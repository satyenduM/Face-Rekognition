from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import boto3
import os

def google_drive_authenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def get_image_files_from_drive(drive, folder_id):
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    image_files = []
    for file in file_list:
        if file['mimeType'] in ['image/jpeg', 'image/png']:
            image_files.append({'id': file['id'], 'title': file['title']})
            print(f"Retrieved {file['title']}")
    return image_files

def upload_image_from_drive_to_s3(s3, bucket_name, drive, file_id, image_name):
    downloaded_file = drive.CreateFile({'id': file_id})
    downloaded_file.GetContentFile(image_name)
    with open(image_name, 'rb') as file_data:
        s3.upload_fileobj(file_data, bucket_name, image_name)
    print(f"Uploaded {image_name} to S3 bucket {bucket_name}.")
    os.remove(image_name)


def compare_faces(bucket, source_image, target_image_files, output_file, matched_images_bucket, s3, drive):
    rekognition = boto3.client('rekognition')
    matched_images = []
    with open(output_file, "w") as file:
        for image_file in target_image_files:
            image_name = image_file['title']
            print(f"Processing image {image_name}...")
            upload_image_from_drive_to_s3(s3, bucket, drive, image_file['id'], image_name)
            response = rekognition.compare_faces(
                SourceImage={'S3Object': {'Bucket': bucket, 'Name': source_image}},
                TargetImage={'S3Object': {'Bucket': bucket, 'Name': image_name}},
                SimilarityThreshold=0 
            )
            is_matched = False
            for face_comparison in response['FaceMatches']:
                similarity = face_comparison['Similarity']
                if similarity >= 90:
                    file.write(f"Match found in image {image_name} with similarity: {similarity}%\n")
                    print(f"Match found in image {image_name} with similarity: {similarity}%")
                    matched_images.append(image_name)
                    is_matched = True
                else:
                    file.write(f"Similarity in image {image_name} is {similarity}%, below the match threshold.\n")
            
            if not is_matched:
                print(f"No match found for {image_name}, deleting from S3...")
                s3.delete_object(Bucket=bucket, Key=image_name)
            else:
                print(f"Matched image {image_name}, moving to {matched_images_bucket}...")
                copy_source = {'Bucket': bucket, 'Key': image_name}
                s3.copy_object(CopySource=copy_source, Bucket=matched_images_bucket, Key=image_name)
                s3.delete_object(Bucket=bucket, Key=image_name)

    return matched_images

if __name__ == "__main__":
    folder_id = '1Lqkgpa1E7_0ObdI9UKHxq7Y_uImKEVRz'
    bucket_name = 'face-rekognition2'
    matched_images_bucket_name = 'resultbucket0'
    reference_face_image = 'face.jpg'

    print("Authenticating with Google Drive...")
    drive = google_drive_authenticate()
    print("Retrieving image files from Google Drive...")
    image_files = get_image_files_from_drive(drive, folder_id)

    s3 = boto3.client('s3')
    print("Comparing faces...")
    matched_images = compare_faces(bucket_name, reference_face_image, image_files, "output_log.txt", matched_images_bucket_name, s3, drive)

    print("Face matching process complete.")
