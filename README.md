# cdktf-poc
Small PoC for CDK for Terraform under a Docker container with docker-compose

The resources will not be applied (no confirmation). Only the "plan" will be output.

Setup AWS credentials:
Edit the [Dockerfile](Dockerfile) and update `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables.

To build the image:
```
COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up -d --build
```

To run the image for debugging:
```
docker run -ti --entrypoint sh cdk-docker_cdk -c bash
```
