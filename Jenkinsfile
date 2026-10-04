pipeline {

    agent any

    environment {
        PYTHON = 'C:\\Users\\laxmi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
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
                bat 'docker --version'
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
                echo 'Running automated tests...'

                bat '''
                    cd backend
                    set PYTHONPATH=.
                    "%PYTHON%" -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                bat '''
                    docker build -t jobportal-backend:latest ./backend
                '''
            }
        }
    }

    post {

        success {
            echo '======================================'
            echo 'JOB PORTAL CI PIPELINE SUCCESSFUL'
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