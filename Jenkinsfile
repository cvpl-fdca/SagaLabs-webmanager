pipeline {
    agent { label 'SagaLabs1' }
    parameters {
        string(name: 'ENV', defaultValue: 'development', description: 'Environment to deploy')
    }
    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
    }
    options {
        skipDefaultCheckout() // Disable the declarative 'Checkout SCM' step
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Check Docker Installation') {
            steps {
                script {
                    // Check if Docker is installed
                    def dockerInstalled = sh(script: 'which docker', returnStatus: true) == 0
                    // If Docker is not installed, then echo a message
                    if (!dockerInstalled) {
                        error('Docker is not installed. Please install Docker before running this pipeline.')
                    } else {
                        echo 'Docker is installed, proceeding with the pipeline.'
                    }
                }
            }
        }

        stage('Check Docker Compose Installation') {
            steps {
                script {
                    // Check if Docker Compose is installed
                    def dockerComposeInstalled = sh(script: 'which docker-compose', returnStatus: true) == 0
                    // If Docker Compose is not installed, then echo a message
                    if (!dockerComposeInstalled) {
                        error('Docker Compose is not installed. Please install Docker Compose before running this pipeline.')
                    } else {
                        echo 'Docker Compose is installed, proceeding with the pipeline.'
                    }
                }
            }
        }

        stage('Clone GitHub repository') {
            steps {
                sh "git clone --branch ${params.ENV} https://github.com/cvpl-fdca/SagaLabs-webmanager.git ."
            }
        }

        stage('Get .env file') {
            steps {
                withCredentials([file(credentialsId: 'env-file-webmanager', variable: 'ENV_FILE_PATH')]) {
                    sh '''
                        cp "${ENV_FILE_PATH}" .env
                    '''
                }
            }
        }

        stage('Populate .env file') {
            steps {
                sh "echo BRANCH_NAME=${BRANCH_NAME} > .env"
            }
        }

        stage('Docker Compose Build and Run') {
            steps {
                sh 'docker-compose up --force-recreate --build -d'
            }
        }
    }
}
