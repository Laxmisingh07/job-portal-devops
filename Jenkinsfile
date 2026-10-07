pipeline {

    agent any

    environment {
        PYTHON = 'C:\\Users\\laxmi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        DOCKER = 'C:\\Users\\laxmi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'

        TRIVY = 'C:\\Users\\laxmi\\AppData\\Local\\Microsoft\\WinGet\\Links\\trivy.exe'

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
                bat '"%TRIVY%" --version'
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

                    if errorlevel 1 (
                        echo Tests failed!
                        exit /b 1
                    )
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Job Portal backend Docker image...'

                bat '''
                    "%DOCKER%" build ^
                        -t %DOCKER_IMAGE%:latest ^
                        -t %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        ./backend

                    if errorlevel 1 (
                        echo Docker image build failed!
                        exit /b 1
                    )

                    echo Docker image built successfully.
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running Trivy security scan...'

                bat '''
                    "%TRIVY%" image ^
                        --scanners vuln ^
                        --severity HIGH,CRITICAL ^
                        --ignore-unfixed ^
                        %DOCKER_IMAGE%:latest

                    if errorlevel 1 (
                        echo Trivy security scan detected HIGH or CRITICAL vulnerabilities.
                        exit /b 1
                    )

                    echo Trivy security scan completed successfully.
                '''
            }
        }
    }

    post {

        success {
            echo '======================================'
            echo 'JOB PORTAL CI PIPELINE SUCCESSFUL'
            echo '======================================'
            echo 'All automated tests passed.'
            echo 'Docker image built successfully.'
            echo 'Trivy security scan completed.'
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