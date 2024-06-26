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
                sshagent(credentials: ['ssh-credentials-id']) {
                    sh '''
                        set -e
                        echo "Connecting to remote server"
                        ssh -o StrictHostKeyChecking=no root@31.128.42.103 <<EOF
                        set -e
                        echo "Connected to remote server"
                        cd movies
                        echo "Pulled latest code"
                        git pull
                        echo "Building Docker image"
                        docker build -t app .
                        echo "Running Docker container"
                        docker run -d -p 8000:8000 app
                        echo "Deployment completed"
                        EOF
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
