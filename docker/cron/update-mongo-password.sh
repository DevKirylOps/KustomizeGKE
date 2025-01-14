#!/bin/bash

ENV=${ENV:-dev}
DEPLOYMENT_APP=${DEPLOYMENT_APP:-app}

# Retrieve current data from Kubernetes secret
MONGO_USER=$(kubectl get secret ${ENV}-mongo-credentials -o=jsonpath='{.data.mongo-user}' | base64 --decode)
MONGO_PASS=$(kubectl get secret ${ENV}-mongo-password -o=jsonpath='{.data.mongo-password}' | base64 --decode)
MONGO_HOST=$(kubectl get secret ${ENV}-mongo-credentials -o=jsonpath='{.data.mongo-uri}' | base64 --decode)

# Password gen
NEW_PASS=$(tr -dc '0-9' </dev/urandom | head -c 7)

mongosh "mongodb://${MONGO_USER}:${MONGO_PASS}@${MONGO_HOST}:27017" --eval "db.getSiblingDB('${MONGO_USER}').updateUser('${MONGO_USER}', {pwd: '${NEW_PASS}'})"

if [ $? -ne 0 ]; then
  echo "Error updating the user in MongoDB. Exiting."
  exit 1
fi

# Updating Kubernetes secret
echo "Updating the Kubernetes secret '${ENV}-mongo-credentials'..."
kubectl create secret generic ${ENV}-mongo-password \
  --from-literal=mongo-password="${NEW_PASS}" \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart deployment
DEPLOYMENT_NAME="${ENV}-${DEPLOYMENT_APP}"
echo "Restarting the deployment '${DEPLOYMENT_NAME}'..."
kubectl rollout restart deployment "${DEPLOYMENT_NAME}"

echo "Script executed successfully!"

