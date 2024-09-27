multibranchPipelineJob('wonderland-white-rabbit') {
  branchSources {
    branchSource {
      source {
        giteaSCMSource {
          id('1')
          credentialsId('gitea-access-token')
          repoOwner("${OWNER}")
          repository('white-rabbit')
          serverUrl("http://gitea:3000")
          traits {
            headWildcardFilter {
              includes('PR-*')
              excludes('')
            }
          }
        }
      }
    }
  }
  configure { node ->
    def traits = node / sources / data / 'jenkins.branch.BranchSource' / source / traits
    traits << 'org.jenkinsci.plugin.gitea.BranchDiscoveryTrait' {
      strategyId('3')
    }
    traits << 'org.jenkinsci.plugin.gitea.OriginPullRequestDiscoveryTrait' {
      strategyId('2')
    }
    def triggers = node / triggers / 'com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger'
    triggers.appendNode('spec', '* * * * *')
    triggers.appendNode('interval', '60000')
  } 
}