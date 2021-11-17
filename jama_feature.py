import math
import threading
from datetime import datetime, timedelta
#from Mysqlconn import Mysqlconn
from api.api_common import api_calls
#from UpdateDatabase import UpdateDatabase

from utils import MyLogger,MyConfigParser
from data_reshape import data_reshape
#from concurrent.futures import ThreadPoolExecutor,as_completed



class JamaData:
    def __init__(self, projectId, jama_itemtypes, G_parameter, loghandle):
        self.projectId = projectId
        self.loghandle = loghandle
        self.G_parameter = G_parameter
        self.jama_itemtypes = jama_itemtypes

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

    def get_features(self, projectId, feature_type_id):
        features = []
        features = self.rest_api.getResource(resource="abstractitems", suffix="", \
            params=None, callback=data_reshape.getFeatures, endless=False)

        return features

    def get_upstreamrelated(self, itemId):
        #### Get all upstream
        upstreamrelated = ""
        upstreamrelated = self.rest_api.getResource(resource="items", suffix="/%s/upstreamrelated"%(itemId), \
            params=None, callback=data_reshape.getUpstreamRelated)

        return upstreamrelated

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
            params={"project":projectId,"startAt":0,"maxResults":50,"itemType":item_type_id}, callback=data_reshape.getAllRequirements, endless=False)

        return allrequirements

    def Get_allfeatuers(self):
        feature_type_id = self.getType("feat")

        self.P_allfeatures = self.get_features(self.projectId, feature_type_id)
        self.loghandle.info(self.P_allfeatures)

    def get_futher_information_requirements(self, maindata):
        coveredTeams = ["Industrial Design", "Strategic Alliances", "PM", "PMM"]  # Teams that don't require testcase
        result = maindata
        for req in result:
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
