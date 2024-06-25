pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/sbin:/usr/bin:/sbin:/bin"
    }
    stages {
        stage('Checkout') {
            steps {
                sh 'git clone -b main https://github.com/jmblx/movies.git'
            }
        }
        stage('Check Docker Path') {
            steps {
                sh 'which docker'
                sh 'docker --version'
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
