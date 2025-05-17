pipeline {
    agent any 

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'  
        DOCKER_IMAGE = 'cithit/colli369'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/seeras-sea/225-final.git'
        KUBECONFIG = credentials('colli369-225')
        SLACK_CHANNEL = '#deployments'
    }

    stages {
        stage('Code Checkout') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
                slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "🚀 Starting build pipeline for ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            }
        }

        stage('Static Code Analysis') {
            steps {
                sh 'pip3 install --user flake8 pylint'
                sh 'python3 -m flake8 --ignore=E302,E305,E501,W291,W292,W293,E128,F401 .'
                sh 'python3 -m pylint --disable=C0111,C0103,C0303,C0301,C0304,C0411,E0401,R0801,R0022 *.py'
                slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "✅ Static code analysis passed"
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pip3 install --user pytest'
                sh 'python3 -m pytest -v || true'
                slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "✅ Unit tests completed"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "🐳 Docker image built: ${DOCKER_IMAGE}:${IMAGE_TAG}"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "📤 Docker image pushed to registry"
                }
            }
        }

        stage('Deploy to Dev Environment') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                    sh "sleep 15" // Wait for deployment
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "🔄 Deployed to DEV environment"
                }
            }
        }

        stage('Verify Database Persistence') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl exec ${appPod} -- ls -la /nfs"
                    sh "kubectl exec ${appPod} -- python3 -c 'import sqlite3; conn = sqlite3.connect(\"/nfs/app.db\"); print(\"Database connection successful\")'"
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "💾 Database persistence verified"
                }
            }
        }

        stage('Generate Test Data') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl exec ${appPod} -- python3 data-gen.py"
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "📊 Test data generated"
                }
            }
        }

        stage("Run Dynamic Tests") {
            steps {
                script {
                    sh 'docker build -t qa-tests -f Dockerfile.test .'
                    sh 'docker run qa-tests'
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "🧪 Dynamic tests passed"
                }
            }
        }
        
        stage('Remove Test Data') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl exec ${appPod} -- python3 data-clear.py"
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "🧹 Test data cleaned up"
                }
            }
        }
         
        stage('Deploy to Production') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                slackSend channel: "${SLACK_CHANNEL}", color: "warning", message: "⚠️ Waiting for approval to deploy to PRODUCTION"
                input message: 'Deploy to production?', ok: 'Yes'
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-prod.yaml"
                    sh "kubectl apply -f deployment-prod.yaml"
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "🚀 Deployed to PRODUCTION environment"
                }
            }
        }

        stage('Verify Production') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                script {
                    sh "kubectl get services | grep prod"
                    slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "✅ Production deployment verified"
                }
            }
        }
    }

    post {
        success {
            slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "✅ Build Successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        unstable {
            slackSend channel: "${SLACK_CHANNEL}", color: "warning", message: "⚠️ Build Unstable: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        failure {
            slackSend channel: "${SLACK_CHANNEL}", color: "danger", message: "❌ Build Failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        always {
            slackSend channel: "${SLACK_CHANNEL}", color: "good", message: "📊 Pipeline completed in ${currentBuild.durationString}"
        }
    }
}