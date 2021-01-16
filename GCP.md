# Configure Zone
```gcloud config set compute/zone us-central1-f```

#  Kubernetes Engine using the Spinnaker tutorial sample application
```
gcloud container clusters create spinnaker-tutorial \
    --machine-type=n1-standard-2
```
# IAM
## create service account
```
gcloud iam service-accounts create spinnaker-account \
    --display-name spinnaker-account
```
