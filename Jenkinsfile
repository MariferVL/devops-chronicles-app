pipeline {
    agent any

    environment {
        // Define the location of your docker-compose file
        DOCKER_COMPOSE_FILE = "docker/docker-compose.yml"
        // Docker Hub username 
        DOCKER_HUB_USER = "marifervl"
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the repository's main branch
                git branch: 'feature/jenkins-pipeline', url: 'https://github.com/MariferVL/devops-chronicles-app.git'
            }
        }
        stage('Build Images') {
            steps {
                echo "Building Docker images using docker-compose..."
                // Build images for web and db as defined in your docker-compose file
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} build"
            }
        }
        stage('Test') {
            steps {
                // Placeholde for tests
                echo "No automated tests available at the moment."
            }
        }
        // stage('Deploy') {
        //     steps {
        //         echo "Deploying application using Ansible playbook..."
        //         // Execute the Ansible playbook to deploy the application.
        //         // The playbook (deploy.yml) is located in the ansible/ directory and the inventory in ansible/inventory.
        //         // We inject the docker_hub_token from Jenkins credentials.
        //         withCredentials([string(credentialsId: 'ansible-docker-hub-token', variable: 'DOCKER_HUB_TOKEN')]) {
        //             sh "ansible-playbook -i ansible/inventory ansible/deploy.yml --extra-vars 'docker_hub_token=${DOCKER_HUB_TOKEN}'"
        //         }
        //     }
        // }

        stage('Check Ansible Files') {
            steps {
                script {
                    if (fileExists('ansible/playbook.yml')) {
                        echo "Ansible playbook found, proceeding with deployment..."
                    } else {
                        error "Ansible playbook not found! Skipping deployment."
                    }
                }
            }
        }

    }
    
    post {
        success {
            echo "Pipeline executed successfully."
        }
        failure {
            echo "Pipeline execution failed. Please review the logs."
        }
    }
}
