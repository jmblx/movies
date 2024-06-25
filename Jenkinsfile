pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                sh 'git clone -b main https://github.com/jmblx/movies.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    docker.image('python:3.11').inside {
                        sh 'python -m venv venv'
                        sh './venv/bin/pip install --upgrade pip'
                        sh './venv/bin/pip install -r requirements.txt'
                    }
                }
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
                    def app = docker.build('movies-app', '.')
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
