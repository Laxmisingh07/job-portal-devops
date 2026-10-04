pipeline {

    agent any

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

                bat 'python --version'
                bat 'git --version'
                bat 'docker --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'

                bat '''
                    cd backend
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated tests...'

                bat '''
                    cd backend
                    set PYTHONPATH=.
                    pytest -v
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