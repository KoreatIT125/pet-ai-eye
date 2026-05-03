pipeline {
    agent any

    environment {
        MODEL_DIR = "models/eye_model_final"
        MODEL_FILE = "best.pt"
        MODEL_PATH = "${MODEL_DIR}/${MODEL_FILE}"

        // Jenkins Credentials "Secret file" ID로 업로드한 모델 파일을 복사
        MODEL_SECRET_FILE_CREDENTIALS_ID = "petmediscan_eye_best_pt"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Git Repository 체크아웃 중...'
                checkout scm
            }
        }

        stage('Prepare Model') {
            steps {
                echo '🧠 모델 파일 준비 중...'
                sh '''
                    set -e
                    mkdir -p "${MODEL_DIR}"

                    if [ -f "${MODEL_PATH}" ]; then
                      echo "✅ 모델 파일 이미 존재: ${MODEL_PATH}"
                      ls -la "${MODEL_PATH}"
                      exit 0
                    fi

                    if [ -n "${MODEL_SECRET_FILE_CREDENTIALS_ID}" ]; then
                      echo "🔐 Jenkins Credentials(Secret file)에서 모델 가져오는 중..."
                    fi
                '''

                script {
                    if (env.MODEL_SECRET_FILE_CREDENTIALS_ID?.trim()) {
                        withCredentials([file(credentialsId: env.MODEL_SECRET_FILE_CREDENTIALS_ID, variable: 'MODEL_SECRET_FILE')]) {
                            sh '''
                                set -e
                                mkdir -p "${MODEL_DIR}"
                                cp "$MODEL_SECRET_FILE" "${MODEL_PATH}"
                                echo "✅ Secret file -> ${MODEL_PATH}"
                                ls -la "${MODEL_PATH}"
                            '''
                        }
                    } else {
                        sh '''
                            set -e
                            if [ -f "${MODEL_PATH}" ]; then
                              exit 0
                            fi
                            echo "❌ 모델 파일이 없습니다: ${MODEL_PATH}"
                            echo "   Jenkins Credentials에 'petmediscan_eye_best_pt' (Secret file) 등록 필요"
                            exit 1
                        '''
                    }
                }
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
            steps {
                echo '🚀 Docker 컨테이너 재배포 중...'
                sh '''
                    docker stop petmediscan-ai-eye || true
                    docker rm petmediscan-ai-eye || true
                    
                    docker run -d \
                        --name petmediscan-ai-eye \
                        --network petmediscan-infra_petmediscan-network \
                        -p 5000:5000 \
                        -e MODEL_VERSION=eye_model_final \
                        -e MODEL_PATH=/app/models/eye_model_final/best.pt \
                        -e SERVICE_TYPE=eye \
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
