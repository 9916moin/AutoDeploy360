pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "moin22/autodeploy360"
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/9916moin/AutoDeploy360.git'
            }
        }

        stage('Test') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip --break-system-packages || true
                pip3 install -r requirements.txt --break-system-packages || true
                pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop autodeploy360 || true
                docker rm autodeploy360 || true
                docker run -d -p 5000:5000 --name autodeploy360 ${DOCKER_IMAGE}:latest
                '''
            }
        }

    }
}