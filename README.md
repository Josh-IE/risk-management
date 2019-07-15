# Risk Management App

## Introduction

The risk management web app is a platform that lets Insurers define custom data models for their risktypes. This helps Insurers in collecting and storing various data without having to directly map the expected data type and structure to database columns. A risktype is referred to as a risk data model in the app.

## Stack

The app was built and tested against:

* Javascript Runtime: Node.js v8.10
* Frontend SPA: Vue.js v2.5.2
* Backend Language: Python v3.6.8
* Backend Framework: Django v2.2
* Backend API: Django Rest Framework v3.9.0
* Database: Postgresql v9.6
* Scripting: Bash
* Deployment: Zappa v0.48.2

## Database

The database models were designed in such a way that the Insurers can create custom risktypes/risk data models without the need to alter the database design in order to accomodate additional risktypes at any point in the future. There are 5 Django Models->Tables that makes this possible and their descriptions can be found below.

* Client: This represents the Insurer.
* RiskModel: This represents the attributes a custom risk data model belonging to a client. Attributes include the text on the risk model form submit button, the summary text about the risk model, the success message returned after risk data submission.
* FieldName: This represents the expected data attributes and type of the risk model. A Field object can belong to only one RiskModel. Field objects can be data attributes like first name, email address, age, amount, avatar with their corresponding field types being text, email, integer, float and file respectively. Other properties like uniqueness, maximum length, field positional order, required etc are available to field objects.
* FieldValue: This represents the data submitted against a risk model Field.
* FormSubmit:This represents the event log of data entry/subbmission against a riskmodel.

It is recommended to use a postgresql database with this app due to the implementation of the postgres specific ArrayField in the ```models.py``` file.

![EER](https://i.imgur.com/UPP4Cwb.png)

## App Logic

### Approach

The app lets users create risk types/models and attach fields to their risk models. Each field has a field type from a list of 17 possible field types. Data submitted against the riskmodel fields are validated with the help of drf serializer classes, based on the field type of the fields and other field attributes like minimun length, uniqueness etc. Submitted Risk data that passes all validation checks are stored in the FieldValue database model, which relates a field to the data sumitted against it.

The api app at ```/api/v1/``` exposes 3 endpoints.

### /risk_model

* GET: Returns a list of risk models with their fields.
* GET /id: Retrieves a risk model with its nested fields.
* POST: Creates a risk model.
* PUT /id: Updates a risk model. Existing fields can be deleted by excluding them from the payload.

### /risk_data

* POST: Creates data against a risk model, by validating and inserting the data into the FieldValue Model table. The form_submit_id is returned if successful.
* GET /id: Retrieves a submitted risk model data using the form_submit_id returned after a successful /risk_data POST request.

### /risk_data_log(?risk_model=risk_model_id)

* GET: Returns a list of **successful** risk data submission events. The risk_model query param is used as a filter.

### Validation

Data posted via the /risk_data endpoint is validated against the risk model fields by making use of a the the drf serializer class that validates the field type. For example, if an insurers custom risk model has a field with field type email, the risk data posted against this field is validated using the django rest framework EmailField serializer. Outside the serializer validation, there are custom validation rules like the unique rule, where the data is considered invalid if it was earlier stored in a **successful** risk data submission.

The app currently supports the 17 field types listed below.

* array: ListField serializer
* checkbox: BooleanField serializer
* date: DateField serializer
* email: EmailField serializer
* file: FileField serializer
* float: FloatField serializer
* multiselect: MultipleChoiceField serializer
* number: IntegerField serializer
* password: CharField serializer
* radio ChoiceField serializer
* regex: RegexField serializer
* select ChoiceField serializer
* switch: BooleanField serializer
* text: CharField serializer
* textarea: CharField serializer
* time: TimeField serializer
* url: URLField serializer

### Data Submission Logging

On a ```/risk_data``` POST event, an entry is first logged in the FormSubmit database table. During the risk data validation step, the fields of the risk model are iterated, on each run, the datum corresponding to the current field in the loop is validated. If the validation is successful, the datum is stored by the FieldValue model. If all the individual validation checks are passed, the success attribute of the form submit entry is updated to ```True``` and the submission is considered a success. But if one of the datum validation fails, the loop is ended immediately and the submission is considered to be failed.

GET requests to the```/risk_data_log``` and ```/risk_data``` endpoints as well as the field uniqueness validation check only considers successful submissions. For example, if the name field is unique, and the datum 'John' is to be validated against this field, if 'John' already exists in the database table under a successful submission, the validation fails, but if 'John' exists under a failed submission, the validation passes, because failed submissions are not considered as valid submissions.

## Frontend Vue.js SPA

The web app is built with Vue.js and themed with the Vuetify material framework. It has 6 views and is powered by the backend api.
The views and their respective functions are listed below.

* Risk Model List ```/```: Landing page. Displays the list of risk models.
* Risk Model Create ```/risk/create```: Displays the risk model create form.
* Risk Model Edit ```/risk/edit/{id}```: Displays the risk model edit form.
* Risk Data Create ```/risk/form/{id}```: Displays the risk data create form.
* Risk Data Event ```/risk/log/{id}```: Displays the list of risk data submission events.
* Risk Data ```/risk/data/{id}```: Displays a submitted risk data.

View Screenshots here: [App Screenshots](https://imgur.com/a/RDn1jKT)

## Project Structure

The project directory has the structure  below.

```tree
.
├── Dockerfile
├── config
│   ├── ***
│   ├── settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
├── deployment
│   ├── credentials
│   ├── dev.env
│   ├── env.json
│   ├── prod.env
│   └── scripts
│       ├── build_docker_image.sh
│       ├── deploy_zappa.sh
│       ├── manage_zappa.sh
│       ├── post_deploy.sh
│       ├── redeploy_zappa.sh
│       ├── setup.sh
│       └── update_zappa.sh
├── manage.py
├── quiz.py
├── requirements
│   ├── development.txt
│   └── production.txt
├── risk_model_api
│   ├── fixtures
│   │   └── app_data.json
│   ├── management
│   │   └── commands
│   │       └── configure_web_app.py
│   ├── migrations
│   │   └── ***
│   ├── models.py
│   ├── tests
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   ├── test_utils.py
│   │   └── test_views.py
│   ├── utils
│   │   ├── serializer_helpers.py
│   │   └── utils.py
│   └── v1
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
├── web-app
│   ├── build
│   │   ├── ***
│   │   └── webpack.base.conf.js
│   ├── config
│   │   ├── ***
│   │   └── index.js
│   ├── dist
│   │   ├── index.html
│   │   └── web-app-static
│   ├── package.json
│   └── src
│       ├── api-services
│       │   ├── riskdata.service.js
│       │   ├── riskdatalog.service.js
│       │   └── riskmodel.service.js
│       ├── components
│       │   └── ***
│       ├── main.js
│       ├── router
│       │   └── index.js
│       └── utils.js
└── zappa_settings.json
```

The Vue.js project directory ```web-app``` sits in the repository root. The assets directory ```web-app/dist``` is listed in the Django STATICFILES_DIRS and TEMPLATES['DIRS'] settings, to enable Django find the built assets when collectstatic is run and to serve the built index.html file from the Django app.

* ```config/```: This is the Django root directory, containing the settings, ```urls.py``` and ```wsgi.py``` modules.
* ```deployment/```: Contains the Docker/Zappa deployment scripts and example env files.
* ```requirements/```: Contains python environment requirement files.
* ```risk_model_api/```: risk model app.
* ```risk_model_api/fixtures/app_data.json```: Optional sample risk model data, loaded into the database during deployment.
* ```risk_model_api/management/commands/configure_web_app.py```: Django command that truncates all tables and loads app_data.json into the database.
* ```risk_model_api/tests/```: Contains the ```risk_model_api``` app tests.
* ```risk_model_api/utils/```: Contains helper Classes and functions used in the app.
* ```web-app/```: The Vue.js spa project.
* ```web-app/build/webpack.base.conf.js```: The webpack base configuration file. The API_URL and STATIC_S3_BUCKET constants are defined here from the environment variables.
* ```web-app/config/index.js```: Here the build assetsSubDirectory was renamed from static to web-app-static, to make it easy to identify the web-app assets in the STATIC storage directory after collectstatic is run. The assetsPublicPath is set to the STATIC_S3_PATH environment variable in build mode. If this variable is undefined, it defaults to '/'.
* ```web-app/dist/```: The vue.js assets directory, created during build.
* ```web-app/src/api-services```: Contains services for making requests to the backend.
* ```web-app/src/components```: Contains the vue components.
* ```web-app/src/main.js```: Axios default url is set here.
* ```web-app/src/router/index.js```: The routes rendering the 6 views are mapped to their components here.
* ```web-app/src/utils.js```: Helper functions are defined here.
* ```quiz.py```: The ```quiz.py``` code I used to solve the debugging quiz.
* ```zappa_settings.json```: Zappa settings file.

## Environment Variables

The environment variables help to configure both the Django and the Vue.js projects. Some are required for the Django project alone, some are required for the Vue.js project alone, some are required when deploying with zappa while some are not required, as they have safe defaults in the code. The ```deployment/``` directory has examples for the prod, dev and lambda environments.
When deploying with zappa, the ```env.json``` file should exist in an s3 bucket(private), as it is required for running the django app in the aws lambda environment. If you prefer not to use this file, there are other methods for setting lambda environment variables, as described in the zappa docs https://github.com/Miserlou/Zappa#setting-environment-variables.

### Description of Environment Variables

Variable | Use | Django | Vue.js | Local | Zappa | Optional | Deafult |
------------ | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
API_URL | Backend url used by Vue.js. |N|Y|Y|N|N|
CORS_ORIGIN_WHITELIST | Origin of the Vue.js app, if hosted on a host or port different from the Django app. |Y|N|Y|N|N|127.0.0.1:8080|
DJANGO_ALLOWED_HOSTS | Django Allowed hosts. |Y|N|Y|Y|Y|*|
DJANGO_DATABASE_URL | Connection url of the database server. |Y|N|Y|Y|N|sqlite:///db.sqlite3|
DJANGO_DEBUG | Django Debug state. |Y|N|Y|Y|Y|True|
DJANGO_MEDIA_ROOT | Storage path of media files. |Y|N|Y|N|Y|media|
DJANGO_SECRET_KEY | Django secret key. |Y|N|Y|N|Y|{some random string}|
DJANGO_SETTINGS_MODULE | Django settings module. |Y|N|N|Y|N|config.settings.dev|
DJANGO_STATIC_ROOT | Storage path of static files. |Y|N|Y|N|Y|static|
FIELD_MAX_LENGTH | Maximum possible length of a risk datum. |Y|N|Y|Y|Y|1000|
STATIC_S3_BUCKET | s3 public bucket for storing static and media files.  |Y|N|N|Y|N||
STATIC_S3_PATH | Public url to s3 bucket. https://{STATIC_S3_BUCKET}.s3.amazonaws.com/. This is used as the assetsPublicPath during zappa deployment npm build. It defaults to '/'. |N|Y|N|Y|N|/|

## Local Setup

You may use 2 separate terminals in local environment setup. One for running Django and the other for running Vue.js.

* clone the repository

    ```bash
    git clone https://github.com/Josh-IE/risk-management.git
    ```

* cd into the repository root

    ```bash
    cd risk-management
    ```

### In Vue.js terminal

* cd into the vue app

    ``` bash
    cd web-app
    ```

* install packages

    ```bash
    npm install
    ```

* set environment variables

    ```bash
    export API_URL=http://localhost:8000/api/v1/
    ```

* run development server

    ```bash
    npm run dev
    ```

### In Django terminal

* activate your virtual environment

* install requirements

    ``` bash
    pip install -r requirements/development.txt
    ```

* set environment variables

    ```bash
    export CORS_ORIGIN_WHITELIST=http://localhost:8080
    export DJANGO_DATABASE_URL={engine}://{user}:{pass}@{host}:{port}/{database}
    ```

* migrate database

    ```bash
    python manage.py migrate risk_model_api
    ```

* load optional sample data

    ```bash
    python manage.py configure_web_app
    ```

* run server

    ```bash
    python manage.py runserver
    ```

The Vue.js web app and Django Api app should now be available at http://localhost:8080 and http://localhost:8000/api/v1 respectively.

### Tests

```bash
coverage run manage.py test
```

## Zappa Deployment

A serverless deployment approach is used in this project. The serverless approach is favored because the burden of infinite scaling and production environment maintenance is transferred to AWS Lambda. Zappa is used to achieve this in the deployment scripts.

### Prerequisites

* Linux machine with about 3GB of available disk space, at least 1GB of free ram and/or some swap space as fallback (if non ssd drive).
* Docker.
* Logged in as a Linux user that belongs to the docker group. This allows the deployment scripts execute docker without sudo priviledges. To add your linux user to the docker group, run ```sudo usermod -aG docker your-user```, logout, then log back in.
* IAM user with a policy that has a wide set of permissions (poses security risk). You can initially test the deployment with the ```AministratorAccess``` policy, and then narrow down the permissions to only what is required by Zappa/Lambda. Unfortunately, I dont have enough intel on the minimum scope of permissions required by Zappa.

    The credentials of this user is to be stored in the local credentials file ```~/.aws/credentials```, under the profile ```[zappa]```. You can use the sample ```deployment/credentials``` file as inspiration. If you choose to use a different profile name, be sure to update the ```profile_name``` key in the ```zappa_settings.json``` file, the AWS_PROFILE arg in the ```deployment/scripts/deploy_zappa.sh```, ```deployment/scripts/manage_zappa.sh```, ```deployment/scripts/redeploy_zappa.sh``` and ```deployment/scripts/update_zappa.sh``` scripts.

    #### NB

    The remote env and static s3 buckets must be created in the same region used in the credentials file, else botocore may get an AuthorizationHeaderMalformed or S3RegionRedirector error when trying to retrieve the remote environment variables or write static and media files. For example, if you go with the sample ```deployment/credentials``` template, which is configured for region ```us-east-1```, then the buckets must be created in region ```us-east-1``` (N. Virginia).

* Private aws s3 bucket for storing the json file containing the environment variables used by the django app in the remote lambda environment. Bucket region must be the same as aws credentials region.
* Public aws s3 bucket for storing static and media files. Bucket region must be the same as aws credentials region.

  You will need to:

  * update the bucket's cors configuration; to enable fetching assets from the django app which resides in a different origin.

  * update the bucket policy to allow hotlinking of its objects. Please exercise caution with this. I enabled it so that the app user can have a public url of uploaded media files. If a sensitive file is uploaded to the app, the file become accessible over the public web.

  You can inspect and and use the sample configuration below.

  CORS Configuration

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <CORSRule>
      <AllowedOrigin>*</AllowedOrigin>
      <AllowedMethod>GET</AllowedMethod>
      <MaxAgeSeconds>3000</MaxAgeSeconds>
      <AllowedHeader>Authorization</AllowedHeader>
  </CORSRule>
  </CORSConfiguration>
  ```

  Bucket Policy

  ```json
  {
      "Version": "2008-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Principal": "*",
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::{your-static-bucket-name}/*"
          }
      ]
  }
  ```

  **Disclaimer**
  It is important to note that the configuration and IAM user priviledges used in this guide is purely indicative. To configure an environment safely, you must be familiar with all the parameters and their meanings.

### Environment variables

Create a .env file in the project root. The .env file must contain API_URL and STATIC_S3_PATH keys. You can use the ```deployment/prod.env``` file as inspiration.

* The right hand side of the API_URL key can be set to any value or left empty because the deployment script will update the value with the api gateway url obtained from ```zappa deploy```.
* The STATIC_S3_PATH should be set to the public url of the public s3 bucket used for storing static files. The format is usually ```https://{bucket-name}.s3.amazonaws.com/```. Note the trailing slash.

Create a json file containing the Django environment variables in the private s3 bucket.
The environment variables are used to configure the Django app in the remote lambda environment. The json file must have the ```DJANGO_DATABASE_URL```, ```DJANGO_SECRET_KEY```, ```DJANGO_SETTINGS_MODULE``` and ```STATIC_S3_BUCKET``` keys set. You can use ```deployment/env.json``` as inspiration.

* The DJANGO_DATABASE_URL should be set to the database connection url.

* The DJANGO_SETTINGS_MODULE must be set to ```"config.settings.prod"```.

* The STATIC_S3_BUCKET should be set to the name of the public bucket created to store static files .

### Configure Zappa

Update the following keys in the zappa settings file.

* profile_name: the aws credential profile. If you followed the ```deployment/credentials``` template, your profile is "zappa".  Use "default" if no profile was used in the ~/.aws/credentials file.

* remote_env: the s3 file system path to the lambda environment variables file. Format ```"s3://{bucket-name}/{file-name}.json"```.

* s3_bucket: name of the bucket where zappa temporarily stores the zipped project. Zappa creates this bucket if it doesnt exist.

### Deployment

This project has 4 scripts responsible for the Deploy, Manage, Update and Redeploy deployment operations. Their functions and usage are summarized below.

NB:

This guide assumes your terminal is in the project root. Run ```pwd``` to verify.

### Deploy

The deployment script ```deployment/scripts/deploy_zappa.sh``` does a number of things.

Build Docker
The zappa deploy script builds a docker image, named ```britecore-zappa``` using the Dockerfile. The container run from this image is the working environment from where zappa would be deployed. The working environment is of importance because it is an environment that closely replicates the remote AWS lambda environment where the code is deployed. This image is based on https://github.com/lambci/docker-lambda/blob/master/python3.6/build/Dockerfile and https://github.com/lambci/docker-lambda/blob/master/nodejs8.10/build/Dockerfile.

Mounts the current directory and the ~/.aws/ directory on the docker container(working environment).

Creates virtual environment and installs requirements.
Creates a virtual environment named ```ve``` and installs requirements/production.txt.

Deploys Zappa
Deploys zappa and updates the value of the API_URL key in the .env file with the Api gateway url returned by ```zappa deploy```.

Builds Vue.js SPA
Sets the environment variables in .env, installs npm packages, builds the Vue.js assets, updates zappa to include the newly built files.

Manage Django app
Migrate the database, truncate the database and load the app_data.json fixtures, collectstatic files into the static s3 bucket.

#### Usage

make the deploy script executable

```bash
chmod +x deployment/scripts/deploy_zappa.sh
```

run the deployment script
NB: This script needs only to be ran once per machine.

```bash
./deployment/scripts/deploy_zappa.sh
```

The deployment url would be echoed on the terminal, after the run. The pattern is usually ```https://{prefix}.execute-api.{region}.amazonaws.com/dev```. You can always run ```zappa status``` in the ```zappashell```(more info below) to retrieve the API Gateway URL. Visit this url on your browser to access the serveless app.

[![asciicast](https://asciinema.org/a/ETA7epU2uvoymlfPLnDj0WEM2.svg?sanitize=true&autoplay=1&speed=10)](https://asciinema.org/a/ETA7epU2uvoymlfPLnDj0WEM2?sanitize=true&autoplay=1&speed=10)

APP URL: https://5em21vp8sc.execute-api.us-east-1.amazonaws.com/dev
API URL: https://5em21vp8sc.execute-api.us-east-1.amazonaws.com/dev/api/v1/

### Manage

This script ```deployment/scripts/manage_zappa.sh``` runs the ```britecore-zappa``` image and grants shell access to the working environment (container). This script should be run only if the deploy script has been initially ran, as its purpose is to run the docker image and manage the zappa deployment that was triggered by the deploy script.
The shell is formatted to look like the shell below, with the prompt set to ```zappashell``` to remind the user they are in the docker working environment. All Zappa commands are available here. Use ```exit``` to exit the working environment/docker container/zappashell.

```console
zappashell> zappa undeploy -y
```

#### Usage

make the manage script executable

```bash
chmod +x deployment/scripts/manage_zappa.sh
```

run the manage script

```bash
./deployment/scripts/manage_zappa.sh
```

### Update

The update script ```deployment/scripts/update_zappa.sh``` is used for shipping code changes to the deployed app running in the lambda environment. Behind the abstraction, this command calls the ```zappa update``` command. It is highly recommended to use this script rather than the zappa update command, as it also handles the running of the migrate command, pip install, npm install and collectstatic commands, which are necessary commands that should follow code updates on deployed Django and Vue.js projects.
NB: This script should only be run if the deploy script has been initially ran, as its purpose is to update the docker image with code changes and manage the zappa deployment that was triggered by the deploy script.

#### Usage

make the manage script executable

```bash
chmod +x deployment/scripts/update_zappa.sh
```

run the manage script

```bash
./deployment/scripts/update_zappa.sh
```

### Redeploy

The redeploy script ```deployment/scripts/redeploy_zappa.sh``` is used to deploy a project that was initially deployed and then undeployed. This is different from the deploy script as it doesnt build the docker image and it doesnt call the configure_web_app command which truncates the tables.
Relevance of this script
Ideally, the deploy script should be run only once per machine(for initial setup), and the manage script should be responsible for both undeploying(```zappa undeploy -y```) and redeploying(```zappa deploy```) the project, but in a likely case where zappa is not deployed on a custom domain, but relies on the randomly assigned AWS Api Gateway Url(which is the case in this project), it is very important to redeploy after an undeploy using this script, because the assignment of a new url will require a chain of post-deploy commands to be executed, which are taken care of by the redeploy script. The post deploy commands are:

* updating the API_URL environment variable in the .env file
* building the Vue.js assets
* updating zappa to account for the newly built assets
* running the migrate command
* running the colllect static command

NB:

* This script should be run only after the deploy script must have been initially ran, as it runs a container from the image built by the deploy script.
* The zappa project must have been undeployed in the manage shell before redeploy can be run.

#### Usage

make the manage script executable

```bash
chmod +x deployment/scripts/redeploy_zappa.sh
```

run the manage script

```bash
./deployment/scripts/redeploy_zappa.sh
```

## FAQ

1. Can I run ```manage.py``` commands in the zappashell/docker container, since the repository is mounted in the container.

    I advise against this, because by default, the ```manage.py``` and ```wsgi.py``` files use ```config.settings.dev``` as the ```DJANGO_SETTINGS_MODULE```. You will have to set the full list of non optional django environment variables anytime you access the shell, to successfully run ```manage.py``` commands without issues.

2. Can I run zappa manage --{env} 'makemigrations' in the zappashell?

    No you cant. Zappa commands are ran on the read-only file system AWS lambda environment, causing commands that write files to fail. You have to run commands like this outside zappa and then update the zappa deployment using the update script.

3. How do I undeploy the app? I cant find a script for that.

    Access the zappshell by running the ```./deployment/scripts/manage_zappa.sh``` script. Once in the shell, run ```zappa undeploy -y```. It is important to note that the currently assigned api gateway url will be lost.

4. Do I need to run the update script before the redeploy script?

    No, you dont have to. The Redeploy operation runs with the latest code base.

5. npm gets killed during deploy or undeploy.

    You may need more ram. Check your ram usage during script operation.

6. I get tar errors during docker build step 4.

    You may be out of disk space. Run ```df -h``` to verify.

7. Why Docker? Cant zappa commands be executed from my local file system.

    Docker is used to build an image that closely resembles the live AWS Lambda environment. All required packages and their dependencies are present in the docker image, saving you many hours of potential environment debugging issues.

8. Are these deployment scripts and processes required if I use a custom domain?

    If a custom domain is used, the deploy script will be run only once; to build the docker image.  The manage script will be used to gain zappashell access for installing python requirements, installing npm packages, re-building assets and pushing code to the remote lambda environment. The redeploy script will not be neccesary because the API_URL would be static and not require an update after every ```zappa deploy```. The update script will be optional, but helpful as it automates the necessary code update and post-deploy chain of commands.
    To sum this up, all scripts but the redeploy script will be relevant.

9. Are there potential security vulnerabilities in the deployment?

    Yes, there are 3 of them:
      * The cors policy of the static assets bucket allows all origins.
      * The objects in the static bucket are exposed to the public web.
      * The npm process is run as the root user in the docker container.

Inspired by Edgar Roman's tutorial https://romandc.com/zappa-django-guide/.