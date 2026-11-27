pipeline {
    agent any

    options {
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    environment {
        IMAGE = 'aceest-fitness'
        TAG = "${env.BUILD_NUMBER}"
        VENV = '.venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                bat 'python -m venv %VENV%'
                bat '%VENV%\\Scripts\\python -m pip install --upgrade pip'
                bat '%VENV%\\Scripts\\pip install -r requirements-dev.txt'
            }
        }

        stage('Lint') {
            steps {
                bat '%VENV%\\Scripts\\flake8 app.py tests'
            }
        }

        stage('Unit Tests') {
            steps {
                bat '%VENV%\\Scripts\\pytest --junitxml=reports\\junit.xml --cov=app --cov-report=xml:reports\\coverage.xml --cov-fail-under=90'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t %IMAGE%:%TAG% -t %IMAGE%:latest .'
            }
        }

        stage('Smoke Test') {
            steps {
                bat 'docker rm -f aceest-smoke 2>nul || exit 0'
                bat 'docker run -d --name aceest-smoke -p 5055:5000 %IMAGE%:%TAG%'
                powershell '''
                    $ok = $false
                    foreach ($i in 1..30) {
                        try {
                            $r = Invoke-RestMethod http://localhost:5055/health
                            if ($r.status -eq "healthy") { $ok = $true; break }
                        } catch {}
                        Start-Sleep 1
                    }
                    if (-not $ok) { throw "app did not become healthy" }
                    $body = @{ weight = 70; program = "Fat Loss (FL)" } | ConvertTo-Json
                    $c = Invoke-RestMethod -Method Post -Uri http://localhost:5055/calories -ContentType "application/json" -Body $body
                    if ($c.calories -ne 1540) { throw "unexpected calories: $($c.calories)" }
                    Write-Host "smoke test passed"
                '''
            }
            post {
                always {
                    bat 'docker logs aceest-smoke 2>nul || exit 0'
                    bat 'docker rm -f aceest-smoke 2>nul || exit 0'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
        success {
            echo "Build ${env.BUILD_NUMBER} passed - image ${env.IMAGE}:${env.TAG}"
        }
        failure {
            echo 'Build failed, check the stage logs above'
        }
    }
}
