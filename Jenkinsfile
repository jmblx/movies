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
                sshCommand remote: [
                    user: 'root',
                    host: '31.128.42.103',
                    password: 'R&gfk3OXyGeh',
                    allowAnyHosts: true
                ], command: '''
                    set -e
                    set -x
                    cd movies
                    git pull
                    docker build -t app .
                    docker run -d -p 8000:8000 app
                '''
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
