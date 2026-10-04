pipeline {

agent any

environment {
    PYTHON = 'C:\\Users\\laxmi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    DOCKER = 'C:\\Users\\laxmi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'

    DOCKER_IMAGE = 'laxmi93243334/jobportal-backend'
}

stages {

    stage('Checkout') {
        steps {
            echo 'Checking out Job Portal source code...'
            checkout scm
        }
    }

    stage('Environment Check') {
        steps {
            echo 'Checking development environment...'

            bat '"%PYTHON%" --version'
            bat 'git --version'
            bat '"%DOCKER%" --version'
        }
    }

    stage('Install Dependencies') {
        steps {
            echo 'Installing Python dependencies...'

            bat '''
                cd backend
                "%PYTHON%" -m pip install --upgrade pip
                "%PYTHON%" -m pip install -r requirements.txt
            '''
        }
    }

    stage('Run Tests') {
        steps {
            echo 'Running automated backend tests...'

            bat '''
                cd backend
                "%PYTHON%" -m pytest -v tests
            '''
        }
    }

    stage('Docker Build') {
        steps {
            echo 'Building Job Portal backend Docker image...'

            bat '''
                "%DOCKER%" build -t %DOCKER_IMAGE%:latest ./backend
            '''
        }
    }

    stage('Docker Push') {
        steps {
            echo 'Pushing Docker image to Docker Hub...'

           withCredentials([
             usernamePassword(
                 credentialsId: 'dockerhub-credentials', 
             usernameVariable: 'DOCKER_USERNAME', 
             passwordVariable: 'DOCKER_PASSWORD'
              ) 
             ]) {

                bat '''
                    echo %DOCKER_PASSWORD% | "%DOCKER%" login -u %DOCKER_USERNAME% --password-stdin
                    "%DOCKER%" push %DOCKER_IMAGE%:latest
                    "%DOCKER%" logout
                '''
            }
        }
    }
}

post {

    success {
        echo '======================================'
        echo 'JOB PORTAL CI PIPELINE SUCCESSFUL'
        echo 'Docker image pushed to Docker Hub.'
        echo '======================================'
    }

    failure {
        echo '======================================'
        echo 'JOB PORTAL CI PIPELINE FAILED'
        echo 'Check the console output.'
        echo '======================================'
    }
}


}
