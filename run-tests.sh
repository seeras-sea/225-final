#!/bin/bash

# Get the Flask service IP
FLASK_IP=$(kubectl get service flask-dev-service -o jsonpath='{.spec.clusterIP}')

echo "Flask service IP: $FLASK_IP"

# Force rebuild the test image
echo "Building test Docker image..."
docker build --no-cache -t qa-tests -f Dockerfile.test .

# Verify the image has the requests library
echo "Verifying requests library installation..."
docker run --rm qa-tests pip list | grep requests

# If requests is not installed, install it directly
if [ $? -ne 0 ]; then
    echo "Installing requests library in the container..."
    docker run --rm qa-tests pip install requests
    # Save the updated container as a new image
    CONTAINER_ID=$(docker run -d qa-tests sleep 10)
    docker commit $CONTAINER_ID qa-tests
    docker stop $CONTAINER_ID
fi

# Run the tests
echo "Running tests against Flask service at http://$FLASK_IP:5000"
docker run --network=host -e FLASK_URL=http://$FLASK_IP:5000 qa-tests
