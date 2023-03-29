import os, boto3
from dotenv import load_dotenv as ENV_LOAD

# constants
ENV_LOAD()
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
BUCKET_NAME  = os.getenv('BUCKET_NAME')

# client end-point
client = boto3.client('s3', endpoint_url=ENDPOINT_URL)

# write
def upload_file(filename, filecontent, show_status=True):
    try:
        client.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=filecontent.encode()
        )
        print("Uploaded" if show_status else "") 
    except:
        print("Error uploading file") 
        

# reading
def read_file(filename):
    """
    read file and `return` the content if success
    """
    try:
        response = client.get_object(
            Bucket=BUCKET_NAME,
            Key=filename,
        )
        return response['Body'].read().decode()
    except:
        return None

# test case
# file = 'note.txt'
# upload_file(file)
# read = read_file(file)
# print(read)