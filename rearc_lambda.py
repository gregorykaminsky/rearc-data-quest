import requests
from bs4 import BeautifulSoup
import boto3
import os 
import io

def lambda_handler(event, context):
    #source url
    url = 'https://download.bls.gov/pub/time.series/pr'
    bucket_name = 'rearc-project'

    #getting the html from the source webpage
    page = requests.get(url, allow_redirects=True).text

    #beautifulsoup is used to parse this html
    soup = BeautifulSoup(page, 'html.parser')

    #stores all the files that are in the source
    source_dict = {}
    for node in soup.find_all('a'): 
        href = node.get('href')
        #saving only the correct urls - skipping the url pointing to the root
        if href.split('/')[-2] == 'pr':
            name = href.split('/')[-1]
            header = requests.head(url + '/' + name, allow_redirects=True).headers
            #only last-modified metadata is necessary
            source_dict[name] = {'Last-Modified':header['Last-Modified']}  

    #stores all the files currently in the destination s3 bucket
    destination_dict = {}
    s3 = boto3.resource('s3', aws_access_key_id=os.getenv('aws_access_key'),
        aws_secret_access_key=os.getenv('aws_secret_key'))
    for file in s3.Bucket(bucket_name).objects.all():
        obj = s3.Object(bucket_name,file.key)
        if 'last-modified-in-source' in obj.metadata:
            destination_dict[file.key] = {'Last-Modified': obj.metadata['last-modified-in-source']}

    #delete all the files in the destination that are not in the source
    for name in destination_dict:
        if name not in source_dict:
            print('Deleted file: ' + name)
            response = s3.Object(bucket_name,name).delete()
            print(response)

    '''
        if the file exists in destination and source
        and the Last-Modified date is identical - then do nothing, 
        otherwise copy the file from source to destination 
    '''
    for file_name in source_dict:
        if (file_name in destination_dict and 
            destination_dict[file_name]['Last-Modified'] == source_dict[file_name]['Last-Modified']):
            continue
        else:
            obj = s3.Object(bucket_name,file_name)
            data = requests.get(url + '/' + file_name, allow_redirects=True).content
            obj.upload_fileobj(Fileobj = io.BytesIO(data),
                            ExtraArgs={"Metadata": {"last-modified-in-source": header['Last-Modified']}})
            