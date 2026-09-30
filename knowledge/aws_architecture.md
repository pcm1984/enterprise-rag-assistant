# AWS Architecture Guidelines

## Compute

Containerized services should normally run on ECS or EKS when the
application requires container orchestration.

AWS Lambda should be considered for event-driven or short-running
serverless workloads.

## Networking

Public traffic should normally enter through a controlled ingress
layer such as an Application Load Balancer.

Internal services should not be unnecessarily exposed to the public
internet.

## Security

Applications should use IAM roles rather than embedding AWS
credentials in application code.
