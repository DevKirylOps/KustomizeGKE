# Service for write and get data form MongoDB
## This project uses
- K8S (Now hosted on GKE)
- Docker & Docker-Compose
- Kustomize
- Python3.10 (Flask)
- MongoDB 6.0

## Project Structure
#### The project consists of two main folders:
- docker
This directory contains the **Dockerfile**, the **script**, and the application **code** to describe the password update logic and the application itself.
- kustomize/
This directory consist of common files in **base/** and logical fallbacks for each environment in **overlays/**, which in turn are managed **through patches**, using a more flexible layout than simply using variables.

## What can be improved
- Use *.env in Kustomize to create more dynamic templates
- Add volume to StatefulSet
- Migrate to Helm
