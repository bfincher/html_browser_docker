def imageName = 'html_browser_docker_temp'

pipeline {
  agent { label 'docker-docker' }

  stages {
    stage('Install') {
      steps {
        script {
          sh "git config --global user.email 'brian@fincherhome.com' && git config --global user.name 'Brian Fincher'"

          branch = sh(script: 'git branch --show-current', returnStdout: true).trim()
          sh "docker build --build-arg BRANCH=${branch} -t ${imageName} --pull ."
          sh 'mkdir -p config/logs/hb'
          uid = sh(script: 'id -u', returnStdout: true).trim()
          gid = sh(script: 'id -g', returnStdout: true).trim()
          try {
              sh "docker run -d -p 8000:80 -v config:/config -v /:/data1 -e USERID=${uid} -e GROUPID=${gid} -e USERNAME=hb_user -e GROUPNAME=hb_group -e HOMEDIR=/hb --name ${imageName} ${imageName}"
              sh "docker ps -a"
              sh "docker exec ${imageName} /bin/bash -c 'cd /hb; python3 manage.py test'"
          } finally {
              sh "docker container rm -f ${imageName}"
          }
        }
      }
    }
  }

  post {
      always {
          script {
              sh "docker image rm -f ${imageName}"
          }
      }
  }
}
