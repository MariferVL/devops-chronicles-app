pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Terraform Directory') {
            steps {
                sh 'chmod -R u+w terraform'
            }
        }
        
        stage('Terraform Provisioning') {
            steps {
                withCredentials([
                    file(credentialsId: 'tfvars-file', variable: 'TF_VARS_FILE'),
                    file(credentialsId: 'devops-key-pub-cred', variable: 'SSH_PUB_KEY'),
                    usernamePassword(credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh 'cp $TF_VARS_FILE terraform/terraform.tfvars'
                    dir('terraform') {
                        echo "Initializing and applying Terraform..."
                        sh 'terraform init'
                        sh(script: '''
                            set +x
                            terraform plan -var "pub_key_content=$(cat $SSH_PUB_KEY)"
                        ''', returnStdout: true)
                        sh(script: '''
                            set +x
                            terraform apply -auto-approve -var "pub_key_content=$(cat $SSH_PUB_KEY)"
                        ''', returnStdout: true)
                    }
                }
            }
        }

        stage('Capture Terraform Outputs') {
            steps {
                dir('terraform') {
                    script {
                        def tfOutput = sh(script: 'terraform output -json', returnStdout: true).trim();
                        def outputs = readJSON(text: tfOutput);

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

                withCredentials([file(credentialsId: 'devops-key-cred', variable: 'SSH_KEY')]) {
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
                        def flaskEnv = sh(script: "aws ssm get-parameter --name '/devops/FLASK_ENV' --query Parameter.Value --output text", returnStdout: true).trim();
                        def dbUser = sh(script: "aws ssm get-parameter --name '/devops/DB_USER' --query Parameter.Value --output text", returnStdout: true).trim();
                        def dbPass = sh(script: "aws ssm get-parameter --name '/devops/DB_PASS' --with-decryption --query Parameter.Value --output text", returnStdout: true).trim();
                        def dbName = sh(script: "aws ssm get-parameter --name '/devops/DB_NAME' --query Parameter.Value --output text", returnStdout: true).trim();
                        def dbRootPass = sh(script: "aws ssm get-parameter --name '/devops/DB_ROOT_PASS' --with-decryption --query Parameter.Value --output text", returnStdout: true).trim();
                        
                        def envContent = """
                            FLASK_ENV=${flaskEnv}
                            DB_HOST=${env.RDS_ENDPOINT}
                            DB_USER=${dbUser}
                            DB_PASS=${dbPass}
                            DB_NAME=${dbName}
                            DB_ROOT_PASS=${dbRootPass}
                            """.stripIndent().trim();

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
        
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    echo "Logging in to Docker Hub..."
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u ${DOCKER_USER} --password-stdin
                        '''
                }
                sh "docker tag marifervl/devops-chronicles:latest marifervl/devops-chronicles:${BUILD_NUMBER}"
                sh "docker push marifervl/devops-chronicles:latest"
                sh "docker push marifervl/devops-chronicles:${BUILD_NUMBER}"
            }
        }
        
        
        stage('Test') {
            steps {
                echo "No automated tests available at the moment."
            }
        }
        
        stage('Prepare Ansible Inventory') {
            steps {
                dir('ansible') {
                    script {
                        sh '''
                        sed -i "s/<INSTANCE_PUBLIC_IP>/${INSTANCE_PUBLIC_IP}/g" inventory.ini
                        sed -i "s/<RDS_ENDPOINT>/${RDS_ENDPOINT}/g" inventory.ini
                        '''
                    }
                }
            }
        }

        stage('Deploy via Ansible') {
            steps {
                dir('ansible') {
                    sh '''
                        if [ ! -f "${WORKSPACE}/venv_ansible/bin/activate" ]; then
                            rm -rf "${WORKSPACE}/venv_ansible"
                            python3 -m venv --upgrade-deps "${WORKSPACE}/venv_ansible"
                        fi

                        . "${WORKSPACE}/venv_ansible/bin/activate"
                        pip install botocore boto3
                        ansible-playbook -i inventory.ini deploy.yml --extra-vars "db_host=${RDS_ENDPOINT} instance_ip=${INSTANCE_PUBLIC_IP}"
                    '''
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
