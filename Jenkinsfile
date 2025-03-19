pipeline {
	agent any

	environment {
		AWS_REGION = 'us-east-1' 
    	DOCKER_COMPOSE_FILE = "docker/docker-compose.yml"
    	DOCKER_HUB_USER = "marifervl"
	}

	stages {
    	stage('Checkout') {
        	steps {
            	git branch: 'develop', url: 'https://github.com/MariferVL/devops-chronicles-app.git'
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
                        def dbHost = sh(script: "aws ssm get-parameter --name '/devops/DB_HOST' --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbUser = sh(script: "aws ssm get-parameter --name '/devops/DB_USER' --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbPass = sh(script: "aws ssm get-parameter --name '/devops/DB_PASS' --with-decryption --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbName = sh(script: "aws ssm get-parameter --name '/devops/DB_NAME' --query Parameter.Value --output text", returnStdout: true).trim()
                        def dbRootPass = sh(script: "aws ssm get-parameter --name '/devops/DB_ROOT_PASS' --with-decryption --query Parameter.Value --output text", returnStdout: true).trim()

                        def envContent = """
                        FLASK_ENV=${flaskEnv}
                        DB_HOST=${dbHost}
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
            	sh "docker-compose --env-file .env -f ${DOCKER_COMPOSE_FILE} build"
        	}
    	}
   	 
    	stage('Test') {
        	steps {
            	echo "No automated tests available at the moment."
        	}
    	}
   	 
		stage('Check Ansible Files') {
			when {
				expression { fileExists('ansible/playbook.yml') }
			}
			steps {
				echo "Ansible playbook found, proceeding with deployment..."
			}
		}

	}
    
	post {
    	always {
        	sh "rm -f .env"
    	}
    	success {
        	echo "Pipeline executed successfully."
    	}
    	failure {
        	echo "Pipeline execution failed. Please review the logs."
    	}
	}
}
