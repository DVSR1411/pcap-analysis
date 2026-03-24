# Elasticsearch and Kibana on Kubernetes

This guide provides instructions for deploying Elasticsearch and Kibana on Kubernetes using the Elastic Cloud on Kubernetes (ECK) operator.

## Overview

The manifests in this directory define:
- **Elasticsearch**: A single-node Elasticsearch cluster (version 8.13.0)
- **Kibana**: A Kibana instance (version 8.13.0) connected to the Elasticsearch cluster

Both services are deployed in the `elastic-stack` namespace.

## Prerequisites

Before deploying Elasticsearch and Kibana, ensure you have:

1. **Kubernetes Cluster**: A running Kubernetes cluster (v1.24 or later recommended)
2. **kubectl**: Installed and configured to access your cluster
3. **ECK Operator**: The Elastic Cloud on Kubernetes operator installed in your cluster
4. **Sufficient Resources**: 
   - At least 2 CPUs and 2GB RAM available
   - Storage class for persistent volumes

### Installing the ECK Operator

If you don't have the ECK operator installed, install it using:

```bash
kubectl apply -f https://download.elastic.co/downloads/eck/2.12.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.12.0/operator.yaml
```

Verify the operator is running:

```bash
kubectl get pods -n elastic-system
```

## Deployment Instructions

### Step 1: Create the Namespace

```bash
kubectl create namespace elastic-stack
```

### Step 2: Deploy Elasticsearch

```bash
kubectl apply -f elastic.yml
```

Wait for Elasticsearch to be ready:

```bash
kubectl get elasticsearch -n elastic-stack
kubectl get pods -n elastic-stack
```

Check the logs to ensure it started correctly:

```bash
kubectl logs -n elastic-stack quickstart-es-default-0
```

### Step 3: Deploy Kibana

```bash
kubectl apply -f kibana.yml
```

Wait for Kibana to be ready:

```bash
kubectl get kibana -n elastic-stack
kubectl get pods -n elastic-stack
```

## Accessing the Services

### Elasticsearch

Elasticsearch is only accessible within the cluster by default. To access it locally:

```bash
kubectl port-forward -n elastic-stack elasticsearch/quickstart 9200:9200
```

Then access it at `https://localhost:9200`

### Kibana

Forward the Kibana service to your local machine:

```bash
kubectl port-forward -n elastic-stack svc/quickstart-kb-http 5601:5601
```

Access Kibana at `http://localhost:5601`

### Default Credentials

The username is `elastic`. To get the password:

```bash
kubectl get secret -n elastic-stack quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
```

## Manifest Details

### elastic.yml

| Field | Value | Description |
|-------|-------|-------------|
| API Version | `elasticsearch.k8s.elastic.co/v1` | Elasticsearch custom resource API |
| Kind | `Elasticsearch` | Kubernetes resource type |
| Name | `quickstart` | Name of the Elasticsearch cluster |
| Namespace | `elastic-stack` | Kubernetes namespace |
| Version | `8.13.0` | Elasticsearch version |
| Node Count | `1` | Number of Elasticsearch nodes |
| Config | `node.store.allow_mmap: false` | Disables memory-mapped files (useful for testing) |

### kibana.yml

| Field | Value | Description |
|-------|-------|-------------|
| API Version | `kibana.k8s.elastic.co/v1` | Kibana custom resource API |
| Kind | `Kibana` | Kubernetes resource type |
| Name | `quickstart` | Name of the Kibana instance |
| Namespace | `elastic-stack` | Kubernetes namespace |
| Version | `8.13.0` | Kibana version |
| Count | `1` | Number of Kibana replicas |
| Elasticsearch Ref | `quickstart` | References the Elasticsearch cluster |

## Monitoring and Management

### View Resource Status

```bash
kubectl get all -n elastic-stack
```

### Delete the Deployment

To remove Elasticsearch and Kibana:

```bash
kubectl delete -f kibana.yml
kubectl delete -f elastic.yml
kubectl delete namespace elastic-stack
```

## Troubleshooting

### Pod Not Starting

Check pod events and logs:

```bash
kubectl describe pod -n elastic-stack <pod-name>
kubectl logs -n elastic-stack <pod-name>
```

### Insufficient Resources

Check available cluster resources:

```bash
kubectl top nodes
kubectl describe nodes
```

### ECK Operator Not Found

Verify the ECK operator is installed:

```bash
kubectl get pods -n elastic-system
```

### No Initial Master Nodes

Elasticsearch requires a minimum number of nodes. For a single-node cluster, ensure `discovery.type: single-node` or adjust node configuration in the manifest.

## Production Considerations

### For Production Deployments

1. **Multiple Nodes**: Increase the `count` in `nodeSets` for high availability
2. **Storage**: Use persistent volumes with appropriate storage class
3. **Resource Limits**: Configure resource requests and limits
4. **Security**: 
   - Enable HTTPS for Elasticsearch
   - Configure authentication and authorization
   - Use network policies for access control
5. **Monitoring**: Enable Stack Monitoring for health checks
6. **Backups**: Configure snapshot repositories for data backup

## Additional Resources

- [Elastic Cloud on Kubernetes Documentation](https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html)
- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)

## Support

For issues or questions:
- Check Elastic Cloud on Kubernetes [GitHub Issues](https://github.com/elastic/cloud-on-k8s/issues)
- Review [ECK Operator Troubleshooting Guide](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-troubleshooting.html)
