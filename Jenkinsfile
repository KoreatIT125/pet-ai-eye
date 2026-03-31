pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        
        stage('Lint') {
            steps {
                sh '. venv/bin/activate && flake8 . --max-line-length=120'
            }
        }
        
        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest tests/'
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    docker.build("disaster-safety-ai-model:${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying AI model...'
                // TODO: 배포 스크립트
            }
        }
    }
    
    post {
        success {
            echo 'AI Model CI/CD 성공!'
        }
        failure {
            echo 'AI Model CI/CD 실패!'
        }
    }
}
