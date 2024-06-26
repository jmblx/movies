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
                sshagent (credentials: ['ssh-credentials-id']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no root@31.128.42.103 <<EOF
                        cd movies
                        git pull
                        docker build -t app .
                        docker run -d app
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
