# rearc-data-quest
Assigned rearc data quest: https://github.com/rearc-data/quest

### Part 1: AWS S3 & Sourcing Datasets
Link to the s3 bucket: http://rearc-project.s3-website-us-west-2.amazonaws.com/ <br>
The files are displayed using 'index.html' file stored in that bucket. <br><br>
<b>CAUTION:</b> <br>
I didn't have time to make index.html that creates a dynamic list of files. If the names of the files change or if files are removed 
, they will not be updated in that link. 
The script to load the files to the s3 bucket is in the rearc_lambda.py. 
This lambda is uploaded to aws with a terraform script. The files are loaded from the api have a Last-Modified date in the 
metadata. When they are uploaded into an s3 bucket, I create a custom metadata field called: "last-modified-in-source". This field is later used 
to check whether any updates have happened and act accordingly. 

### Part 2: APIs
