pipeline {
  agent any

  environment {
    DOCKERHUB_USER = "dikshyant180"
    IMAGE_NAME     = "hello-app"
    IMAGE_TAG      = "${env.GIT_COMMIT.take(7)}"
    CHART_REPO     = "github.com/DixT-180/hello-app-chart.git"
  }

  stages {
    stage('Checkout app-source') {
      steps {
        checkout scm
      }
    }

    stage('Build image') {
      steps {
        sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
      }
    }

    stage('Push image to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh """
            echo \$DH_PASS | docker login -u \$DH_USER --password-stdin
            docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Update hello-app-chart') {
  steps {
    withCredentials([usernamePassword(credentialsId: 'hello-app-source', usernameVariable: 'GH_USER', passwordVariable: 'GH_PAT')]) {
      sh """
        rm -rf chart-repo
        git clone https://\$GH_USER:\$GH_PAT@${CHART_REPO} chart-repo

        cd chart-repo

        yq -i '.image.tag = "${IMAGE_TAG}"' values.yaml

        git config user.email "jenkins@ci"
        git config user.name "jenkins"

        if git diff --quiet; then
          echo "No changes to commit. Image tag is already ${IMAGE_TAG}."
        else
          git add values.yaml
          git commit -m "Update image to ${IMAGE_TAG}"
          git push https://\$GH_USER:\$GH_PAT@${CHART_REPO} main
        fi
      """
    }
  }
}

  post {
    always {
      sh 'docker logout || true'
    }
    success {
      echo "Pipeline succeeded: pushed ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} and updated hello-app-chart"
    }
    failure {
      echo "Pipeline failed — check console output above for which stage broke"
    }
  }
}