#!/bin/bash
rm -f rearc_lambda.zip
mkdir deploy_rearc
pip install --target deploy_rearc/package requests bs4
zip rearc_lambda.zip rearc_lambda.py
cd deploy_rearc/package; zip -r ../../rearc_lambda.zip .
cd ../..
rm -r deploy_rearc

terraform init
terraform validate
terraform plan
terraform apply --auto-approve