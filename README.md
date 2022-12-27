# rearc-data-quest
Assigned rearc data quest: https://github.com/rearc-data/quest

### Part 1: AWS S3 & Sourcing Datasets
Link to the s3 bucket: http://rearc-project.s3-website-us-west-2.amazonaws.com/ <br>
The files are displayed using 'index.html' file stored in that bucket. <br><br>
<b>CAUTION:</b> <br>
I didn't have time to make index.html that creates a dynamic list of files. If the names of the files change or if files are removed 
, they will not be updated in that link.  <br>
The script to load the files to the s3 bucket is in the rearc_lambda.py. 
This lambda is uploaded to aws with a terraform script. The files are loaded from the api have a Last-Modified date in the 
metadata. When they are uploaded into an s3 bucket, I create a custom metadata field called: "last-modified-in-source". This field is later used 
to check whether any updates have happened and act accordingly. 

### Part 2: APIs
File 'part2.py' does the assigned task. Loaded from source and then uploaded to s3 bucket. No custom metadata field is added so it doesn't interfere with part 1. 

### Part 3: Data Analytics
Done in file 'part3.ipynb'. The negative values where never removed as I wasn't sure what they meant. 


### Part 4: Infrastructure as Code & Data Pipeline with AWS CDK
The rearc_lambda.py is uploaded using a terraform script in main.tf and provider.tf. It is scheduled to run daily at 12:00pm UTC.
I run out of time and didn't implement the sqs queue and the second lambda to read that queue. 
