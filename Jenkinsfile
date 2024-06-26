pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/jmblx/movies.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh './venv/bin/pytest'
            }
        }
        stage('Build and Deploy') {
            steps {
                script {
                    sh 'docker build -t "app" .'
                    sh 'docker run -d -p 8000:8000 --name app-container "app"'
                }
            }
        }
        stage('Remote Deploy') {
            steps {
                sshagent(credentials: ['remote-server']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no root@31.128.42.103 '
                            cd movies && \
                            git pull && \
                            docker build -t "app" . && \
                            docker run -d -p 8000:8000 --rm --name app-container "app"
                        '
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
