# C3 - File Storage Backup for S3
A pythonic CLI based backup utility for backing up a directory of choice to an AWS S3 bucket.

## Features
- Saves last known uploaded document to prevent recusive writing to the cloud
- Declaritive struture using yaml
- Save objects automatically to storage class of choice (reduce object storage cost)
- Hands free cron schduling (ie. Write new objects to cloud at interval specified)

## Dependicies
All Dependicies can be found in ``` requirements.txt ```

## Usage
```
usage: main.py [-h] [-n] [-d] [-f CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -n, --new             Create new Backup Job (required)
  -d, --download        Download all files from S3 bucket (required)
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        Alternate location of config.yaml file. (optional parameter defaults to ./config.yaml)
```
When using flag ``` -n ``` requires a config.yaml file in the C3 root directory. File that follows schema.yaml see config.yaml.sample for demo config file.

## New Job (Upload)
Creates new upload job using cron scheduler based on paramters given in ``` config.yaml ``` file.

## New Download
Creates new download job using cron scheduler based on paramters given in ``` config.yaml ``` file.

## Config - Input
```input``` parameter reflects location of files directory to be backed up along with specified files with corresponding extensions that should be uploaded.
```
input:
  path: "./photos"
  file-extensions:
    - '.jpg'
    - '.png'
```
#
## Config - Target
``` target ``` parameter outlines cloud provider details including bucket storage class and targeted regions.
[Please see support providers below](##Providers)
```
target:
  max-uploaded-file: 100
  max-download-file:
  provider:
    aws:
      region: "us-east-1"
      bucket-name: "test-bucket"
      storage-policy: "STANDARD"
```
``` max-uploaded-file ``` and ``` max-download-file ``` both tak in any Integer to limit maximum number of files uploaded and downloaded from bucket. Leaving value as ``` None ``` results in a limit of upload / download based on the number of objects at play.
#

### Providers
Supported providers
``` 
aws
 ```
 ### AWS Parameters
-  ``` region ``` region symbol name (optional = False)
-  ``` bucket-name ``` bucket name of aws S3 bucket, case and numeric sensitive optional = False)
- ``` storage-class ``` allows for the following case senstive storage policy types optional = False); ``` 'STANDARD'|'REDUCED_REDUNDANCY'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'GLACIER'|'DEEP_ARCHIVE'|'OUTPOSTS' ```
#
## Config - Job
``` job ``` parameter outlines details corresponding to cron job schduling. All fields BUT ```job-desciption``` below are required
```
job:
  job-description: "test backup!"
  runtime:
    at:
      - second: 1
      - minute: 10
      - hour: 2
```

### So wheres the Cron?
C3 relies on the [Schedule](https://pypi.org/project/schedule/) python package and is not truly a Cron job scheduler. Schedule was chosen due to limitations of [CronTab](https://pypi.org/project/python-crontab/). But you maybe asking yourself how do I run C3 in the background?
### nohup is your friend
Basic syntax for converting python script to system process;
- Convert python script to exacutable ``` chmod +x main.py -n ```
- Run the command nohup ``` /path/to/scheduler.py & ``` . The '&' symbol ensures that your script will run in the background as a system process.

More detail can be had from this short [tutorial](https://dev.to/damjand/python-scheduler-a-cron-job-replacement-54ep) by Damjan Dimitrov


