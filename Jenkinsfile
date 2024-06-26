pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/jmblx/movies.git'
            }
        }
        stage('Install Python') {
            steps {
                sh 'apt-get update && apt-get install -y python3.11 python3.11-venv'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python3.11 -m venv venv'
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
                    sh 'docker run -d "app"'
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
