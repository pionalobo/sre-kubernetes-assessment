# Kubernetes System Monitoring Application

A small Kubernetes-based system that periodically collects system metrics and stores them in PostgreSQL. A Flask web application retrieves and displays the latest collected metrics.

## How It Works

The web application runs in Kubernetes and communicates with PostgreSQL through an internal Kubernetes Service.

A Kubernetes CronJob periodically starts a metrics collector. The collector gathers CPU, memory, disk, hostname, operating system, and timestamp information and stores the results in PostgreSQL.

PostgreSQL uses a PersistentVolumeClaim so collected data remains available if the database pod is replaced.

The web application runs with two replicas, with a Horizontal Pod Autoscaler configured to scale between 2 and 5 replicas based on CPU utilisation.

## Components

- **Flask + Gunicorn** — Web application
- **PostgreSQL** — Backend datastore
- **Kubernetes CronJob** — Periodic metrics collection
- **PersistentVolumeClaim** — PostgreSQL data persistence
- **Horizontal Pod Autoscaler** — Web application scaling
- **Ingress** — HTTP routing
- **Kubernetes Dashboard** — Cluster and workload monitoring
- **Kubernetes Secret** — Database credentials

## Requirements

- Docker Desktop
- Minikube
- kubectl
- Git

## Setup

##### Start Minikube:

```
minikube start --driver=docker
```
##### Enable the required add-ons:
```
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard
```
##### Create the database Secret:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\create-secret.ps1
````
##### Build the application images:
```
docker build -t sre-web:latest .\app
docker build -t sre-collector:latest .\collector
```
##### Load the images into Minikube:
```
minikube image load sre-web:latest
minikube image load sre-collector:latest
```
##### Deploy the Kubernetes resources:
```
kubectl apply -f kubernetes/
```
##### Check the workloads:
```
kubectl get pods -n sre-assessment
```
##### Access the Application: 

The application is accessed from the host browser using kubectl port-forward:
```
kubectl port-forward -n sre-assessment service/web 8080:80
```
Open:
http://localhost:8080

The application displays the latest CPU, memory, disk, hostname, operating-system information, and collection timestamp.

##### Minikube IP

The Kubernetes Ingress is also configured using the Minikube IP. The Minikube IP can be checked with:
```
minikube ip
```
In the tested Windows + Minikube Docker-driver environment, the Minikube IP was not directly reachable from the Windows browser. Therefore, http://localhost:8080 through kubectl port-forward is the reliable browser access method used for this project.

##### Kubernetes Dashboard:

The Kubernetes Dashboard can be launched with:
```
minikube dashboard
```
It provides a graphical view of the Kubernetes cluster, including:

Pods
Deployments
Services
Jobs and CronJobs
Resource utilisation
Cluster workloads
Verification

##### Check the CronJob:
```
kubectl get cronjob -n sre-assessment
```
##### Check the HPA:
```
kubectl get hpa -n sre-assessment
```
##### Check collected metrics:
```
kubectl exec -n sre-assessment deployment/postgres -- psql -U sreuser -d sredb -c "SELECT * FROM system_metrics ORDER BY collected_at DESC LIMIT 5;"
```
##### Security:
Database credentials are stored in a Kubernetes Secret.
The real Secret is excluded from Git.
Web and collector containers run as non-root.
Container capabilities are dropped where configured.
CPU and memory requests/limits are defined.