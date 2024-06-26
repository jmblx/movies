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
                withCredentials([usernamePassword(credentialsId: 'ssh-credentials-id', passwordVariable: 'SSH_PASSWORD', usernameVariable: 'SSH_USERNAME')]) {
                    sh '''
                        set -x
                        sshpass -p $SSH_PASSWORD ssh -o StrictHostKeyChecking=no $SSH_USERNAME@31.128.42.103 <<EOF
                        set -e
                        set -x
                        cd movies || exit 1
                        git pull || exit 1
                        docker build -t app . || exit 1
                        docker run -d -p 8000:8000 app || exit 1
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
