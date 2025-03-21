FROM jenkins/jenkins:lts

USER root

RUN apt update && \
    apt install -y docker.io docker-compose unzip ansible wget && \
    rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

RUN wget https://releases.hashicorp.com/terraform/1.11.2/terraform_1.11.2_linux_amd64.zip && \
    unzip terraform_1.11.2_linux_amd64.zip -d /usr/local/bin && \
    rm terraform_1.11.2_linux_amd64.zip

RUN mkdir -p /var/jenkins_home/workspace && \
    chown -R jenkins:jenkins /var/jenkins_home/workspace && \
    chmod -R u+w /var/jenkins_home/workspace
  
RUN mkdir -p /opt/venv_ansible && \
chown -R jenkins:jenkins /opt/venv_ansible && \
chmod -R u+w /opt/venv_ansible

RUN usermod -aG docker jenkins

USER jenkins
