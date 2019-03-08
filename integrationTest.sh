#!/bin/bash

serviceEndpoint=$(aws cloudformation describe-stacks --stack-name resizePDF-$STAGE --query 'Stacks[0].Outputs[?OutputKey==`ServiceEndpoint`].OutputValue' --output text)
echo $serviceEndpoint

python3 test/integration.py serviceEndpoint