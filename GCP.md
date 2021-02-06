## Configure Zone & region
```
gcloud config set compute/zone us-central1-f
gcloud config set compute/region us-central1
```

# create instance
```
gcloud compute instances create www1 \
  --image-family debian-9 \
  --image-project debian-cloud \
  --zone us-central1-a \
  --tags network-lb-tag \
  --metadata startup-script="#! /bin/bash
    sudo apt-get update
    sudo apt-get install apache2 -y
    sudo service apache2 restart
    echo '<!doctype html><html><body><h1>www1</h1></body></html>' | tee /var/www/html/index.html"
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
