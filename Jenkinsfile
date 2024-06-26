pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-u root'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/jmblx/movies.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh './venv/bin/pytest'
            }
        }
        stage('Deploy to Remote Server') {
            steps {
                sshagent(credentials: ['asdfhinou']) {
                    sh '''
                        set -e
                        echo "Connecting to remote server"
                        ssh -o StrictHostKeyChecking=no root@31.128.42.103 << "ENDSSH"
                            set -e
                            echo "Connected to remote server"
                            cd movies
                            echo "Pulled latest code"
                            git pull
                            echo "Removing all Docker containers"
                            docker rm -f $(docker ps -aq) || true
                            echo "Building Docker image"
                            docker build -t app .
                            echo "Running Docker container"
                            docker run -d --init -p 8000:8000 app
                            echo "Deployment completed"
                        ENDSSH
                    '''
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
