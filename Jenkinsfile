pipeline {
    agent any

    environment {
        PIP_CACHE_DIR = "${WORKSPACE}/.pip"
    }

    stages {
        stage('Checkout') {
            steps {
                // Убедитесь, что Jenkins использует установленный Git
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/jmblx/movies']]])
            }
        }
        stage('Install Docker') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker --version'
                    } else {
                        bat 'docker --version'
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python -m venv venv'
                        sh './venv/bin/pip install --upgrade pip'
                        sh './venv/bin/pip install -r requirements.txt'
                    } else {
                        bat 'python -m venv venv'
                        bat '.\\venv\\Scripts\\pip install --upgrade pip'
                        bat '.\\venv\\Scripts\\pip install -r requirements.txt'
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh './venv/bin/pytest'
                    } else {
                        bat '.\\venv\\Scripts\\pytest'
                    }
                }
            }
        }
        stage('Build and Deploy') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker build -t movies-app src'
                        sh 'docker run -d -p 8000:8000 movies-app'
                    } else {
                        bat 'docker build -t movies-app src'
                        bat 'docker run -d -p 8000:8000 movies-app'
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                cleanWs()
            }
        }
    }
}
