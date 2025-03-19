pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        DOCKER_HUB_USER = "marifervl"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Terraform Provisioning') {
            steps {
                dir('terraform') {
                    echo "Initializing and applying Terraform..."
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }
        
        stage('Capture Terraform Outputs') {
            steps {
                dir('terraform') {
                    script {
                        def tfOutput = sh(script: 'terraform output -json', returnStdout: true).trim()
                        def outputs = readJSON text: tfOutput

                        env.INSTANCE_PUBLIC_IP = outputs.instance_public_ip.value
                        env.RDS_ENDPOINT = outputs.rds_endpoint.value
                        echo "Instance Public IP: ${env.INSTANCE_PUBLIC_IP}"
                        echo "RDS Endpoint: ${env.RDS_ENDPOINT}"
                    }
                }
            }
        }
        
        stage('Configure SSH Known Hosts') {
            steps {
                sh '''
                    mkdir -p ~/.ssh
                    ssh-keyscan -H ${INSTANCE_PUBLIC_IP} >> ~/.ssh/known_hosts
                '''
            }
        }
        
        stage('Configure SSH Key') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'devops-key-cred', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        mkdir -p ~/.ssh
                        cp $SSH_KEY ~/.ssh/devops-key
                        chmod 600 ~/.ssh/devops-key
                    '''
                }
            }
        }
        
        stage('Retrieve AWS Parameters and Prepare .env file') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    script {
                        def flaskEnv = sh(script: "aws ssm get-parameter --name '/devops/FLASK_ENV' --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbUser = sh(script: "aws ssm get-parameter --name '/devops/DB_USER' --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbPass = sh(script: "aws ssm get-parameter --name '/devops/DB_PASS' --with-decryption --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbName = sh(script: "aws ssm get-parameter --name '/devops/DB_NAME' --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbRootPass = sh(script: "aws ssm get-parameter --name '/devops/DB_ROOT_PASS' --with-decryption --query Parameter.Value --output text", returnStdout: true).trim()
                        
                        def envContent = """
                        FLASK_ENV=${flaskEnv}
                        DB_HOST=${RDS_ENDPOINT}
                        DB_USER=${dbUser}
                        DB_PASS=${dbPass}
                        DB_NAME=${dbName}
                        DB_ROOT_PASS=${dbRootPass}
                        """
                        writeFile file: '.env', text: envContent
                    }
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                dir('docker') {
                    sh "docker-compose --env-file ${WORKSPACE}/.env -f docker-compose.yml build"
                }
            }
        }
        
        stage('Test') {
            steps {
                echo "No automated tests available at the moment."
            }
        }
        
        stage('Deploy via Ansible') {
            steps {
                dir('ansible') {
                    sh "ansible-playbook -i inventory.ini deploy.yml --extra-vars \"db_host=${RDS_ENDPOINT} instance_ip=${INSTANCE_PUBLIC_IP}\""
                }
            }
        }

    }
    
    post {
        always {
            sh "rm -f ${WORKSPACE}/.env"
        }
        success {
            echo "Pipeline executed successfully."
        }
        failure {
            echo "Pipeline execution failed. Please review the logs."
        }
    }
}
