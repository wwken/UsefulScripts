#!/bin/bash

# Copyright (c) 2016 Ken Wu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# -----------------------------------------------------------------------------
#
# Author: Ken Wu
# Date: 2016 May
#
# Have you felt it is very painful to deal with aws s3 files in command line?
# This script is to increase the programmer/dev ops productivity by short hand most of the commonly used aws s3 commands
#
# Usage:
#   Put these four lines into your bashrc file and source it
#       declare AWS_S3_BASH_RC_DEST=/tmp/bashrc_aws_s3.sh
#       rm "${AWS_S3_BASH_RC_DEST}" 2> /dev/null
#       wget -O "${AWS_S3_BASH_RC_DEST}" -q https://raw.githubusercontent.com/wwken/UsefulScripts/master/bashrc_aws_s3.sh 
#       source "${AWS_S3_BASH_RC_DEST}"
#
# Examples:
#   To ls a aws s3 files/directory
#       sls {S3_BUCKET}
#       sls {S3_BUCKET_OR_FILE}
#
#   To download a aws s3 file (optional with dest download path)
#       sd {S3_BUCKET_OR_FILE}
#       sd {S3_BUCKET_OR_FILE} {LOCAL_DEST_DIRECTORY}
#
#   To cat a aws s3 file on fly
#       sc {S3_BUCKET_OR_FILE}
#
#   To vi a aws s3 file on fly
#       sv {S3_BUCKET_OR_FILE}
#
#

aws_ls_function(){
    aws s3 ls s3://$1
}
alias sls='aws_ls_function'

aws_download_function(){
    declare DOWNLOAD_DEST=./
    if [ -n "${2}" ]
    then
        DOWNLOAD_DEST="${2}"
    fi
    aws s3 cp s3://$1 "${DOWNLOAD_DEST}" || { echo "Download failed"; return 1;}
    return 0
}
alias sd='aws_download_function'

# This is a library function
_aws_download_function_wrapper(){
    declare LOCAL_DEST_FOLDER="/tmp/aws-s3-download/$1"
    mkdir -p "${LOCAL_DEST_FOLDER}"
    aws_download_function $1 "${LOCAL_DEST_FOLDER}"
    return $?
}

aws_cat_function(){
    declare FILE_NAME=`basename "$1"`
    _aws_download_function_wrapper "$1"
    if [ $? -eq 0 ]; then
        cat "/tmp/aws-s3-download/$1/${FILE_NAME}"
    fi
}
alias sc='aws_cat_function'

aws_vi_function(){
    declare FILE_NAME=`basename "$1"`
    _aws_download_function_wrapper "$1"
    if [ $? -eq 0 ]; then
        vi "/tmp/aws-s3-download/$1/${FILE_NAME}"
    fi
}
alias sv='aws_vi_function'