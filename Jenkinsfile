pipeline {
    agent {
        docker { image 'python:3.9' }
    }
    environment {
        PIP_CACHE_DIR = "${WORKSPACE}/.pip"
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/jmblx/movies.git'
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
                    def app = docker.build('movies-app', 'src')
                    app.run('-d -p 8000:8000')
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
