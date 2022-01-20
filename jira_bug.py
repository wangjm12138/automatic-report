import re
from jira import JIRA
from api.api_common import api_calls
from utils import MyLogger,MyConfigParser
from data_reshape import data_reshape

class JamaData:
    def __init__(self, projectId, jama_itemtypes, G_parameter, loghandle, pinumber, hardware):
        self.jira_user = G_parameter["General"]["jirausername"]
        self.jira_apikey = G_parameter["General"]["jirapassword"]
        self.jira_issue = G_parameter["General"]["jiraissue"]


        self.jira = JIRA(options, basic_auth=(user,apikey))

    def get_issue_status(self, issue_number):
        """Function to get issue status"""
        issue = self.jira.issue(issue_number)
        status = issue.fields.status.name
        return status

    def get_issue_priority(self, issue_number):
        """Function to get issue status"""
        issue = self.jira.issue(issue_number)
        priority = issue.fields.priority.name
        return priority

    def get_issue_status_priority(self, issue_number):
        issue = self.jira.issue(issue_number)
        status = issue.fields.status.name
        priority = issue.fields.priority.name
        return status, priority
