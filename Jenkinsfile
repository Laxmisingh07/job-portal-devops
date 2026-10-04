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

                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Docker Push') {
            steps {
                echo 'Logging into Docker Hub and pushing Docker image...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    bat '''
                        echo %DOCKER_PASSWORD% | "%DOCKER%" login -u %DOCKER_USERNAME% --password-stdin

                        if errorlevel 1 (
                            echo Docker Hub login failed!
                            exit /b 1
                        )

                        echo Docker Hub login successful.

                        "%DOCKER%" push %DOCKER_IMAGE%:latest

                        if errorlevel 1 (
                            echo Docker image push failed!
                            "%DOCKER%" logout
                            exit /b 1
                        )

                        echo Docker image pushed successfully.

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
            echo '======================================'
            echo 'All tests passed.'
            echo 'Docker image built successfully.'
            echo 'Docker image pushed to Docker Hub.'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo 'JOB PORTAL CI PIPELINE FAILED'
            echo '======================================'
            echo 'Check the failed stage in the console output.'
            echo '======================================'
        }

        always {
            echo 'CI pipeline execution completed.'
        }
    }
}