pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                sh 'git clone -b main https://github.com/jmblx/movies.git'
            }
        }
        stage('Install Dependencies') {
            agent {
                docker {
                    image 'python:3.11'
                }
            }
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
        stage('Build and Deploy') {
            steps {
                sh 'docker build -t movies-app .'
                sh 'docker run -d -p 8000:8000 movies-app'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
