"""
Convert a heroku environment file into a django env file.

run `heroku config --app gist-core-dev > .env-gist-core-dev` then
`python core/utils/heroku2env.py .env-gist-core-dev .env.dev`
to create a local env file that matches a heroku environment
use `ln -s .env.dev .env` to create a softlink
"""

import sys
import re

blacklisted_variables = [
    "CLINICAL_REVIEW_EMAIL",
    "COMMIT_SHA",
    "DISABLE_COLLECTSTATIC",
    "EMAIL_HOST_PASSWORD",
    "EMAIL_HOST_USER",
    "ENVIRONMENT_NAME",
    "FACEBOOK_PIXEL_ID",
    "FACEBOOK_PIXEL_SCHEDULE_CONSULTATION_ID",
    "FEATURE_FLAG_HEAP_ANALYTICS",
    "FILE_TRANSFER_SERVICE_TOKEN",
    "FILE_TRANSFER_SERVICE_URL",
    "GENEPEEKS_TARGET_INTERVALS",
    "HEAP_ANALYTICS_APP_ID",
    "LOGDNA_KEY",
    "MIN_VGD_SUBJECT",
    "MONGODB_KEEP_BACKUPS",
    "OVERWRITE_ANALYSIS_RUNS",
    "DISPLAY_ALT_PARAM_DETAILS",
    "REDIS_TIMEOUT",
    "REDIS_URL",
    "RELEASE_HOLDING",
    "SCIENCE_REVIEW_EMAIL",
    "SENTIEON_DOCKER_IMAGE",
    "TZ",
    "WORKFLOW_INTERNAL_VARIANTS_SCHEDULE",
]

append_settings = [
    "DJANGO_SETTINGS_MODULE=genepeeks.settings",
    "DOMAIN_NAME=127.0.0.1.xip.io",
    "HOST_PORT=8000",
    "SECURE=False",
    "STATIC_URL=/static/",
]


def convert_variable(line):
    converted = line
    if converted.split(":")[0] in blacklisted_variables:
        return ""  # don't use the variable.
    if converted.endswith('-----BEGIN PRIVATE KEY-----\n'):
        converted = converted.replace('\n', '\\n')
    if ':' not in converted:
        # it's a private key line
        converted = converted.replace('\n', '')

    return converted.replace("  ", "").replace(":", "=", 1).replace("= ", "=")


def heroku2env(heroku_line):
    variable = re.compile("^[A-Za-z0-9].*")
    line = "# "
    if variable.match(heroku_line):
        line = convert_variable(heroku_line)
    else:
        if '-----END PRIVATE KEY-----' in heroku_line:
            line = "\\n" + heroku_line
        else:
            line += heroku_line
    return line

# check if you pass the input file and output file
if sys.argv[1] is not None and sys.argv[2] is not None:
    file_input = sys.argv[1]
    file_output = sys.argv[2]
    with open(file_input) as input_file:  # open heroku settings file
        with open(file_output, 'w') as output_file:  # get the env file ready
            for line in input_file:
                output_file.write(heroku2env(line))
            for line in append_settings:
                output_file.write(line + "\n")
