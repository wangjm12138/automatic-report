

class ETL:
    def __init__(self, allfeatures, allrequirements, projectId):
        self.allfeatures = allfeatures
        self.allrequirements = allrequirements
        self.projectId =  projectId

    def data_cleaning(self):
        feature_defect = {}
        defect_feature = {}
        tmp_key=[]
        for data in self.allrequirements:
            for feature in data['upstreamrelated']:
                tmp_key.append({'feature_documentKey':feature['documentKey'],'feature_name':feature['name'],'id':feature['id']})
                if feature["documentKey"] not in feature_defect:
                    feature_defect[feature['documentKey']]={}
                    feature_defect[feature['documentKey']]['feature_name'] = feature['name']
                    feature_defect[feature['documentKey']]['feature_link'] = "https://jabra.jamacloud.com/perspective.req#/items/%s?projectId=%s"%(feature["id"], self.projectId)
                    feature_defect[feature['documentKey']]['defectlist'] = {}
            for defect in data['defect']:
                if defect["documentKey"] not in defect_feature:
                    defect_feature[defect['documentKey']]={}
                    defect_feature[defect['documentKey']]['defect_name'] = defect['name']
                    defect_feature[defect['documentKey']]['defect_link'] = defect['jira_link']
                    defect_feature[defect['documentKey']]['featurelist'] = {}

                for item in tmp_key:
                    feature_defect[item['feature_documentKey']]['defectlist'].update({defect['documentKey']:{"defect_name":defect['name'],"defect_link":defect["jira_link"]}})
                    defect_feature[defect['documentKey']]['featurelist'].update({item['feature_documentKey']:{"feature_name":item['feature_name'],'feature_link':"https://jabra.jamacloud.com/perspective.req#/items/%s?projectId=%s"%(item["id"], self.projectId)}})
                    #feature_defect[item]["defect_name"] = defect['name']
                    #feature_defect[item]['defect_key'] = defect['documentKey']
                    #feature_defect[item]['defect_link'] = defect['jira_link']
            tmp_key = []

        for feature in self.allfeatures:
            if feature["documentKey"] not in feature_defect:
                feature_defect[feature['documentKey']]={}
                feature_defect[feature['documentKey']]['feature_name'] = feature['name']
                feature_defect[feature['documentKey']]['feature_link'] = "https://jabra.jamacloud.com/perspective.req#/items/%s?projectId=%s"%(feature["id"], self.projectId)
                feature_defect[feature['documentKey']]['defectlist'] = {}



        return feature_defect,defect_feature

    def ETL_output(self):
        feature_defect, defect_feature = self.data_cleaning()
        return feature_defect, defect_feature
