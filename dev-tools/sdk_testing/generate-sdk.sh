#!/bin/bash
# generate-sdk.sh

echo "Checking if API Gateway is up..."
curl --silent --fail http://localhost:8080/health > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: API Gateway is not accessible at http://localhost:8080"
    echo "Please run 'docker-compose up -d' first."
    exit 1
fi

echo "API is up. Generating SDKs with LibLab..."
cd ../sdk
liblab build

if [ $? -eq 0 ]; then
    echo "SDK Generation Complete!"
else
    echo "SDK Generation Failed."
    exit 1
fi
