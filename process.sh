#! /bin/bash
#
# process.sh
# Copyright (C) 2014 vagrant <vagrant@vagrant-ubuntu-trusty-64>
#
# Distributed under terms of the MIT license.
#

bucket=tagtoo_rtb_log

for file in `ls request.log.*|grep -v '.gz'`
do
    i_file=$file
    o_file=`echo ${file}.gz|sed 's/request.log/request.json/'`
    echo "process $i_file"
    python rtb_upload.py $i_file $o_file 

    if [ $? -ne 0 ]
    then
        echo 'process error'
        break
    fi

    echo "processed $i_file"&


    echo "start upload $o_file to gs://$bucket/$o_file" 
    gsutil cp $o_file gs://$bucket/ 

    if [ $? -ne 0 ]
    then
        echo "upload error"
        break
    fi
    echo "upload success"

    echo "remove  $i_file $o_file"
    rm $i_file $o_file
done

