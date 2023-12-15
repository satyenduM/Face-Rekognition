
# Face Recognition with Google Drive and AWS Rekognition

This repository contains a Python script that integrates Google Drive and Amazon Web Services (AWS) Rekognition for an automated face recognition process. The script downloads images from a specified Google Drive folder, uploads them to an AWS S3 bucket, and then uses AWS Rekognition to compare these images with a reference face image. Matched images are identified and are moved to another S3 bucket.

## Features

- Authentication with Google Drive
- Retrieval of image files from a specified Google Drive folder
- Uploading images to AWS S3
- Face comparison using AWS Rekognition
- Logging of matched faces and their similarity scores
- Management of S3 objects based on face match results

## Prerequisites

- Python 3.x
- Google Drive API enabled GCP project
- AWS account with S3 and Rekognition services
- AWS CLI configured with appropriate permissions

## Installation

1. Clone this repository.
2. Install required Python packages:
    ```bash
    pip install PyDrive boto3
    ```
3. Ensure AWS CLI is configured with your AWS credentials.

## Detailed Setup Instructions

### Google Drive Setup

1. **Enable Google Drive API**:
   - Visit the [Google Developers Console](https://console.developers.google.com/).
   - Create a new project or select an existing one.
   - Navigate to "API & Services" > "Dashboard" and click "ENABLE APIS AND SERVICES".
   - Search for "Google Drive API", select it, and click "Enable".

2. **Create Credentials**:
   - In the same project dashboard, go to "Credentials".
   - Click "Create credentials" and choose "OAuth client ID".
   - If prompted, configure the OAuth consent screen.
   - For the application type, select "Desktop app" and give it a name.
   - Once created, download the JSON file containing your credentials.
   - Rename this file to `client_secrets.json` and place it in the same directory as your Python script.

3. **Install PyDrive**:
   - PyDrive is a wrapper library for the Google Drive API. Install it using pip:
     ```bash
     pip install PyDrive
     ```

### AWS Setup

1. **AWS CLI Configuration**:
   - If not already installed, download and install the [AWS CLI](https://aws.amazon.com/cli/).
   - Configure the CLI with your AWS credentials. Run the following command and enter your AWS access key ID, secret access key, and default region:
     ```bash
     aws configure
     ```

2. **Create S3 Buckets**:
   - You need two S3 buckets: one for uploading the images for recognition, and another for storing matched images.
   - You can create these buckets through the AWS Management Console or using the AWS CLI:
     ```bash
     aws s3 mb s3://[bucket-name]
     aws s3 mb s3://[matched-images-bucket-name]
     ```
   - Replace `[bucket-name]` and `[matched-images-bucket-name]` with your desired bucket names.

3. **Install Boto3**:
   - Boto3 is the Amazon Web Services (AWS) SDK for Python. Install it using pip:
     ```bash
     pip install boto3
     ```

4. **Permissions**:
   - Ensure your AWS IAM user has permissions to access S3 and Rekognition services.
   - This typically involves attaching policies like `AmazonS3FullAccess` and `AmazonRekognitionFullAccess` to the IAM user or role you're using.

## Usage

1. Set the `folder_id` in the script to the ID of the Google Drive folder containing the images.
2. Set the `bucket_name` and `matched_images_bucket_name` to your AWS S3 bucket names.
3. Place the reference face image in the same directory as the script and name it (default is `face.jpg`).
4. Run the script:
    ```bash
    python face_recognition_script.py
    ```

## Limitations

- The script processes only JPEG and PNG image formats.

