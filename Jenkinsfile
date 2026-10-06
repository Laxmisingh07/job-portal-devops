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

        stage('Docker Hub Push') {
            steps {
                echo 'Publishing Docker images to Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    powershell '''
                        Write-Host "Logging in to Docker Hub..."

                        $env:DOCKER_PASSWORD | & $env:DOCKER "login" "-u" $env:DOCKER_USERNAME "--password-stdin"

                        if ($LASTEXITCODE -ne 0) {
                            Write-Host "Docker Hub login failed!"
                            exit 1
                        }

                        Write-Host "Docker Hub login successful."

                        Write-Host "Pushing latest image..."

                        & $env:DOCKER "push" "$env:DOCKER_IMAGE`:latest"

                        if ($LASTEXITCODE -ne 0) {
                            Write-Host "Docker Hub latest push failed!"
                            exit 1
                        }

                        Write-Host "Latest image pushed successfully."

                        Write-Host "Pushing build-specific image..."

                        & $env:DOCKER "push" "$env:DOCKER_IMAGE`:$env:BUILD_NUMBER"

                        if ($LASTEXITCODE -ne 0) {
                            Write-Host "Docker Hub build image push failed!"
                            exit 1
                        }

                        Write-Host "Build-specific image pushed successfully."

                        Write-Host "Docker images published successfully."
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
            echo 'All automated tests passed.'
            echo 'Docker image built successfully.'
            echo 'Docker image published to Docker Hub.'
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