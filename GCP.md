## Configure Zone & region
```
gcloud config set compute/zone us-central1-f
gcloud config set compute/region us-central1
```

##  Kubernetes Engine using the Spinnaker tutorial sample application
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
## 
```
export SA_EMAIL=$(gcloud iam service-accounts list \
    --filter="displayName:spinnaker-account" \
    --format='value(email)')
```
export PROJECT=$(gcloud info --format='value(config.project)')
```

# clusterrolebinding
```
kubectl create clusterrolebinding user-admin-binding \
    --clusterrole=cluster-admin --user=$(gcloud config get-value account)
 ```
 ```
 kubectl create clusterrolebinding --clusterrole=cluster-admin \
    --serviceaccount=default:default spinnaker-admin
 ```
