pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "moin22/autodeploy360"
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main',
                    url: 'https://github.com/9916moin/AutoDeploy360.git'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                 sh 'pip3 install -r requirements.txt --break-system-packages --user'
                 sh 'python3 -m pytest tests/ -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo 'Pushing to DockerHub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }

    }

    post {
        success {
            echo 'Pipeline SUCCESS!'
        }
        failure {
            echo 'Pipeline FAILED!'
        }
    }
}