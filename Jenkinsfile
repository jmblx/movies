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
            environment {
                REMOTE_USER = 'root'
                REMOTE_HOST = '31.128.42.103'
                REMOTE_PASS = credentials('your-credentials-id') // заменить на ваш credentials ID
            }
            steps {
                script {
                    def remoteCommand = '''
                        set -e
                        echo "Connected to remote server"
                        cd movies || { echo "Directory not found"; exit 1; }
                        echo "Pulling latest code"
                        git pull || { echo "Git pull failed"; exit 1; }
                        echo "Building Docker image"
                        docker build -t app . || { echo "Docker build failed"; exit 1; }
                        echo "Running Docker container"
                        docker run -d -p 8000:8000 app || { echo "Docker run failed"; exit 1; }
                        echo "Deployment completed"
                    '''

                    sh """
                        sshpass -p ${REMOTE_PASS} ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} <<EOF
                        ${remoteCommand}
                        EOF
                    """
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
