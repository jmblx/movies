pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-u root' // Чтобы иметь root права для установки пакетов
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
