---
title: Kubernetes Deployment
description: Run Nexus Core on Kubernetes. Scalable, resilient, production-grade.
section: deployments
order: 2
---

# Kubernetes Deployment

Run Nexus Core on **Kubernetes**. Scalable, resilient, production-grade.

## Quick Start

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -l app=nexus-core
```

## Helm Chart

```bash
# Add repo
helm repo add skillseekers https://charts.skillseekers.io

# Install
helm install nexus-core skillseekers/nexus-core \
  --set config.name=react \
  --set schedule="0 0 * * 0"
```

## CronJob for Scheduled Scraping

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nexus-core-scrape
spec:
  schedule: "0 2 * * 0"  # Weekly
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: nexus-core
            image: skillseekers/nexus-core:latest
            command:
              - nexus-core
              - scrape
              - --config
              - /config/react.json
            volumeMounts:
              - name: config
                mountPath: /config
              - name: output
                mountPath: /output
          volumes:
            - name: config
              configMap:
                name: nexus-core-configs
            - name: output
              persistentVolumeClaim:
                claimName: nexus-core-output
          restartPolicy: OnFailure
```

## ConfigMap for Configurations

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nexus-core-configs
data:
  react.json: |
    {
      "name": "react",
      "url": "https://react.dev",
      "target": "langchain"
    }
```

## Features

- ✅ **Scalable** - Run multiple jobs in parallel
- ✅ **Resilient** - Automatic retries and failover
- ✅ **Scheduled** - CronJobs for automation
- ✅ **Monitored** - Prometheus metrics available
