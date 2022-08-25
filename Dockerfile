FROM node

ARG TERRAFORM_VERSION=1.1.3
ARG PROJECT_NAME="cdktf-aws-demo"
# Not the proper way to pass the credentials. Should be using docker secrets
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""

RUN apt-get update -y && \
    apt-get install -y unzip wget

################################
# Install Terraform
################################
RUN wget -q https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/local/bin/ && \
    chmod +x /usr/local/bin/terraform

################################
# Install python
################################
RUN apt-get install -y python3-pip && \
    pip3 install --upgrade pipenv

################################
# Install CDK
################################
RUN npm install --global cdktf-cli@latest

ADD ${PROJECT_NAME}/ ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME}
RUN pip3 install -r requirements.txt
RUN cdktf get
RUN cdktf synth
RUN cdktf deploy
