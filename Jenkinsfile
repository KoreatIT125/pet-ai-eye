pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Git Repository 체크아웃 중...'
                checkout scm
            }
        }
        
        stage('Docker Build') {
            steps {
                echo '🐳 Docker 이미지 빌드 중...'
                sh '''
                    docker build -t petmediscan-ai-eye:${BUILD_NUMBER} .
                    docker tag petmediscan-ai-eye:${BUILD_NUMBER} petmediscan-ai-eye:latest
                '''
            }
        }
        
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                echo '🚀 Docker 컨테이너 재배포 중...'
                sh '''
                    docker stop petmediscan-ai-eye || true
                    docker rm petmediscan-ai-eye || true
                    
                    docker run -d \
                        --name petmediscan-ai-eye \
                        --network pet-infra_petmediscan-network \
                        -p 5000:5000 \
                        -v $(pwd)/models:/app/models \
                        petmediscan-ai-eye:latest
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ AI Eye 빌드 및 배포 성공!'
        }
        failure {
            echo '❌ AI Eye 빌드 또는 배포 실패!'
        }
        always {
            echo '🧹 워크스페이스 정리 중...'
            cleanWs()
        }
    }
}
