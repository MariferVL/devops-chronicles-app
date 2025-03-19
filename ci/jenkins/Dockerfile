FROM jenkins/jenkins:lts

USER root

RUN apt update && \
	apt install -y docker-compose && \
	rm -rf /var/lib/apt/lists/*

USER jenkins
