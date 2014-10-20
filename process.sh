#! /bin/bash
#
# process.sh
# Copyright (C) 2014 vagrant <vagrant@vagrant-ubuntu-trusty-64>
#
# Distributed under terms of the MIT license.
#

bucket=tagtoo_rtb_log

for file in `ls request.log*|grep -v '.gz'`
do
    i_file=$file
    o_file=${file}.json.gz
    echo "process $i_file"
    python rtb_upload.py $i_file $o_file && echo "start upload $o_file to gs://$bucket/$o_file" && gsutil cp $o_file gs://$bucket/ && echo "upload end... remove $i_file $o_file" && rm $o_file $i_file&& echo "processed $i_file"&
done

