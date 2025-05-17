#!/bin/bash

# Get the Flask service IP
FLASK_IP=$(kubectl get service flask-dev-service -o jsonpath='{.spec.clusterIP}')

echo "Flask service IP: $FLASK_IP"

# Run the tests with a custom command that installs requests first
echo "Running tests against Flask service at http://$FLASK_IP:5000"
docker run --network=host -e FLASK_URL=http://10.43.39.124:5000 qa-tests /bin/bash -c "pip install requests && python -m pytest test_html_elements.py -v"

