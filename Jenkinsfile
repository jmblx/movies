pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'movies_app_image'
        SSH_CREDENTIALS_ID = 'your-ssh-credentials-id'
        SSH_HOST = '31.128.42.103'
        SSH_USER = 'root'
        SSH_PASSWORD = 'R&gfk3OXyGeh'
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
                    docker.build("${env.DOCKER_IMAGE}", '.')
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${env.DOCKER_IMAGE}").inside {
                        sh 'pytest'
                    }
                }
            }
        }

        stage('Deploy to Server') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sshagent (credentials: [env.SSH_CREDENTIALS_ID]) {
                        sh """
                        sshpass -p "${env.SSH_PASSWORD}" ssh ${env.SSH_USER}@${env.SSH_HOST} << EOF
                        cd /root/movies
                        git pull origin main
                        docker-compose down
                        docker-compose build
                        docker-compose up -d
                        EOF
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                docker.image("${env.DOCKER_IMAGE}").inside {
                    sh 'docker-compose down'
                }
            }
        }
    }
}
