from jenkinsapi import api
import urllib2
import sys
import yaml

class JenkinsInit():
    def __init__(self):
        if len(sys.argv) != 2:
            sys.exit("Usage: ./%s jobname" %sys.argv[0])

        with open('datamap.yml','r') as ymlfile:
            config=yaml.load(ymlfile)

        yamlMeta = (config['datamap'])
        self.jenkinsUrl = yamlMeta['jenkinshost']
        self.user = yamlMeta['jenkinsuser']
        self.token = yamlMeta['token']
        self.sparkRoom = yamlMeta['sparkRoom']

        self.jobName = sys.argv[1]
        self.jenkins = api.Jenkins(self.jenkinsUrl, username=self.user, password=self.token)
        self.job = self.jenkins.get_job(self.jobName)
        self.build = self.job.get_last_build()

    def dataBoot(self):
        # Collect all the metadata
        self.status=self.build.get_status()
        self.jobUrl=self.build.baseurl

    def statusPrinter(self):
        #prints the status to spark room

        data = '{"text": "BUILD %s  JOB: %s  URL %s"}' %(self.status,self.jobName,self.jobUrl)
        req = urllib2.Request(self.sparkRoom, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        for x in f:
            print(x)
        f.close()

    def JenkinsAction(self):

        if self.build.is_good():
            print "The build passed successfully"
            self.dataBoot()
            self.statusPrinter()

        else:
            print "Build Failed"
            self.dataBoot()
            self.statusPrinter()

jenkinsUser = JenkinsInit()
jenkinsUser.JenkinsAction()