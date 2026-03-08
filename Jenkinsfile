pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/pannamrajesh/aceest-devops.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                sh 'flake8 app.py --max-line-length=100'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest tests/ -v --tb=short'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t aceest-fitness:latest .'
            }
        }

    }

    post {
        success {
            echo 'BUILD SUCCESSFUL - ACEest pipeline complete!'
        }
        failure {
            echo 'BUILD FAILED - Check stage logs above'
        }
    }
}