pipeline {
  agent { label 'docker-docker' }

  stages {
    stage('Install') {
      steps {
        script {
          sh "git config --global user.email 'brian@fincherhome.com' && git config --global user.name 'Brian Fincher'"
          sh 'docker image ls'
        }
      }
    }
		
  }
}
