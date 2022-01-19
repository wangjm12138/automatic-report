import re
import math
import threading
from tqdm import tqdm
from datetime import datetime, timedelta
#from Mysqlconn import Mysqlconn
from api.api_common import api_calls
#from UpdateDatabase import UpdateDatabase

from utils import MyLogger,MyConfigParser
from data_reshape import data_reshape
from concurrent.futures import ThreadPoolExecutor,as_completed



class JamaData:
    def __init__(self, projectId, jama_itemtypes, G_parameter, loghandle, pinumber, hardware):
        self.projectId = projectId
        self.loghandle = loghandle
        self.pinumber = pinumber
        self.hardware = hardware
        self.G_parameter = G_parameter
        self.jama_itemtypes = jama_itemtypes
        self.Max_threads = G_parameter['General']["Max_threads"]

        self.Test_all = {}
        self.P_allfeatures  = []
        self.P_allrequirements, self.P_reqcovered = [], {}
        self.rest_api = api_calls(G_parameter = self.G_parameter, loghandle = self.loghandle)

    def getType(self, input_type):
        """Function to get item type"""
        for item_type in self.jama_itemtypes:
            if item_type["type_key"].lower() == input_type.lower():
                return item_type["id"]

    def get_singlefeature(self, feature_id):
        feature = []
        feature = self.rest_api.getResource(resource="abstractitems", suffix="/%s"%(str(feature_id)), \
            params=None, callback=data_reshape.getsingleFeature, endless=False)

        return feature

    def get_singlereq(self, req_id):
        req = []
        req = self.rest_api.getResource(resource="abstractitems", suffix="/%s"%(str(req_id)), \
            params=None, callback=data_reshape.getsingleRequirment, endless=False)

        return req

    # def get_features(self, projectId, feature_type_id):
    #     features = []
    #     features = self.rest_api.getResource(resource="abstractitems", suffix="", \
    #         params=None, callback=data_reshape.getFeatures, endless=True)
    #
    #     return features
    def get_testplans(self, projectId):
        existing_testplans = {}
        existing_testplans = self.rest_api.getResource(resource="testplans", suffix="", \
            params={"project":projectId,"startAt":0,"maxResults":50}, callback=data_reshape.getTestPlans, endless=True)
        return existing_testplans

    def get_testgroups(self, testplanId):
        testgroups = {}
        testgroups = self.rest_api.getResource(resource="testplans", suffix="/%s/testgroups"%(testplanId), \
                params={"startAt":0,"maxResults":50}, callback=data_reshape.getTestGroups, endless=True)
        return testgroups

    def get_testcases(self, testplanId, testgroups):
        #### Get all test plan testcases
        testcases = {}
        with ThreadPoolExecutor(max_workers=int(self.Max_threads)) as executor:
            obj_list = []
            for testgroup in testgroups:
                #obj = executor.submit(self.rest_api.NewgetTestCases,"testplans",testplanId, testgroup, \
                #    params={"startAt":0,"maxResults":50}, endless=True, callback=data_reshape.getTestCases)
                obj = executor.submit(self.rest_api.getResource,resource="testplans", suffix="/%s/testgroups/%s/testcases"%(testplanId, testgroup), \
                        params={"startAt":0,"maxResults":50}, endless=True,callback=data_reshape.getTestCases)
                obj_list.append(obj)

            for future in as_completed(obj_list):
                result = future.result()
                testcases.update(result)
        return testcases

    def get_features(self, projectId, feature_type_id):
        features = []
        features = self.rest_api.getResource(resource="abstractitems", suffix="", \
            params={"project":projectId,"startAt":0,"maxResults":50,"itemType":feature_type_id}, callback=data_reshape.getFeatures, endless=True)

        return features
    def get_upstreamrelated_req(self, itemId):
        #### Get all upstream
        upstreamrelated = ""
        upstreamrelated = self.rest_api.getResource(resource="items", suffix="/%s/upstreamrelated"%(itemId), \
            params=None, callback=data_reshape.getUpstreamRelated_req)

        return upstreamrelated

    def get_upstreamrelated(self, itemId):
        #### Get all upstream
        upstreamrelated = ""
        upstreamrelated = self.rest_api.getResource(resource="items", suffix="/%s/upstreamrelated"%(itemId), \
            params=None, callback=data_reshape.getUpstreamRelated)

    def get_downstreamrelated(self, itemId):
        #### Get all upstream
        downstreamrelated = ""
        downstreamrelated = self.rest_api.getResource(resource="items", suffix="/%s/downstreamrelated"%(itemId), \
            params=None, callback=data_reshape.getDownstreamRelated)

        return downstreamrelated

    def get_downstreamrelated_defect(self, itemId):
        #### Get all upstream
        downstreamrelateddefect = ""
        downstreamrelateddefect = self.rest_api.getResource(resource="items", suffix="/%s/downstreamrelated"%(itemId), \
            params=None, callback=data_reshape.getDownstreamRelateddefect)
        return downstreamrelateddefect

    def get_allrequirements(self, projectId, item_type_id):
        allrequirements = []
        allrequirements = self.rest_api.getResource(resource="abstractitems", suffix="", \
            params={"project":projectId,"startAt":0,"maxResults":50,"itemType":item_type_id}, callback=data_reshape.getAllRequirements, endless=True)

        return allrequirements

    def Get_allfeatuers(self):
        feature_type_id = self.getType("feat")

        self.P_allfeatures = self.get_features(self.projectId, feature_type_id)
        self.loghandle.info(self.P_allfeatures)
        return self.P_allfeatures

    def get_futher_information_requirements(self, maindata):
        coveredTeams = ["Industrial Design", "Strategic Alliances", "PM", "PMM"]  # Teams that don't require testcase
        result = maindata
        for req in tqdm(result):
            #req["status"] = self.get_picklistoptions(req["statusId"])
            #req["downstreamcase_parentlist"] = self.get_downstreamcase_parentlist(req["id"])
            defect = []
            req["upstreamrelated"] = self.get_upstreamrelated(req["id"])
            req["downstreamrelated"] = self.get_downstreamrelated(req["id"])

            if len(req["downstreamrelated"]) > 0:
                for item in req["downstreamrelated"]:
                    defect +=  self.get_downstreamrelated_defect(item["id"])

            req["defect"] = defect

        return result

    def Get_allrequirements(self):

        requirements_type_id = self.getType("req")
        self.P_allrequirements =  self.get_allrequirements(self.projectId, requirements_type_id)
        #self.P_allrequirements =  self.get_singlereq(5942130)
        self.loghandle.info(self.P_allrequirements)
        self.P_allrequirements = self.get_futher_information_requirements(self.P_allrequirements)
        self.loghandle.info(self.P_allrequirements)

        return self.P_allrequirements

    def get_testcases_information_requirements(self, testcases):
        feature = []
        req = []
        for testcase_item in testcases:
            reqs = self.get_upstreamrelated_req(testcase_item["id"])
            for req_item in reqs:



    def Get_PItestplan(self):

        self.loghandle.info("Get project id:%s all testplans"%(self.projectId))
        existing_testplans = self.get_testplans(self.projectId)
        #print(existing_testplans)
        for testplanId in existing_testplans:
            test_plan_name = existing_testplans[testplanId]["name"]
            if self.projectId == "20393":
                pattern1 = re.compile(self.pinumber)
                pattern2 = re.compile(self.hardware)
                m1 = pattern1.search(test_plan_name)
                m2 = pattern2.search(test_plan_name)
                if m1 and m2:
                    print(testplanId)
                    self.Test_all["testplan"] = existing_testplans
                    testgroups = self.get_testgroups(testplanId)
                    #testruns = self.get_testruns(testplanId)
                    testcases = self.get_testcases(testplanId, testgroups)
                    self.Test_all["testplan"] = existing_testplans
                    #self.Test_all["testruns"] = testruns
                    self.Test_all["testcase"] = testcases
        self.testcases_feature = self.get_testcases_information_requirements(self.Test_all["testcases"])
        print(self.Test_all)
