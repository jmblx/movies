pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/jmblx/movies'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("movies-app:${env.BUILD_ID}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'pytest'
                    }
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    docker.withRegistry('', 'DOCKER_HUB_CREDENTIALS') {
                        dockerImage.push("${env.BUILD_ID}")
                        dockerImage.push("latest")
                    }

                    sshagent(credentials: ['server-credentials']) {
                        sh """
                        ssh root@31.128.42.103 'docker pull movies-app:latest && docker run -d -p 8000:8000 movies-app:latest'
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
