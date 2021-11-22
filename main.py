import os
import re
import sys
import pdb
import time
import json
import timeit
import traceback

from word import Word
from datetime import datetime
from api.api_common import api_calls
from data_reshape import data_reshape

from jama_feature import JamaData
from data_cleaning import ETL
from utils import MyLogger,MyConfigParser

def read_config_file():
    """
        Discription:
            get the configuration of Config.ini and save it in G_paramter
    """
    G_parameter = {}
    cfg = MyConfigParser()
    cfg_path = "./config.ini"
    cfg.read(cfg_path)
    sections = cfg.sections()
    for item in sections:
        G_parameter[item] = {}
        for key in cfg[item]:
            text = cfg.get(item, key)
            G_parameter[item][key] = text
    return G_parameter


def read_text():
    """
        Discription:
            get the configuration of Text.ini and save it in Text
    """
    Text = {}
    cfg = MyConfigParser()
    cfg_path = "./Title.ini"
    cfg.read(cfg_path)
    sections = cfg.sections()
    for item in sections:
        Text[item] = {}
        for key in cfg[item]:
            text = cfg.get(item, key)
            Text[item][key] = text
    return Text

def CreateFolders(G_parameter):
    """
        Discription:
            check db/jira, log/%Y%m%d, if not exist, create it
        Parameters:
            param1 - G_paramter comes from Config.ini
    """
    date = time.strftime("%Y%m%d", time.localtime(time.time()))
    LOGFOLDER_PATH = os.path.join(G_parameter['General']['baselogpath'],date)
    if not os.path.exists("db/jira/"):
        os.makedirs("db/jira")
    if not os.path.exists(LOGFOLDER_PATH):
        os.makedirs(LOGFOLDER_PATH)
    return LOGFOLDER_PATH


if __name__ == "__main__":

    jama_projects, jama_itemtypes = [],[]
    ### prepare phase
    G_parameter = read_config_file()
    Text = read_text()
    LOGFOLDER_PATH = CreateFolders(G_parameter)
    LOGGER_CONTROL = MyLogger(name= "main", log_name="main", LOGFOLDER_PATH=LOGFOLDER_PATH)

    #LOGGER_CONTROL.disable_file()
    LOGGER_MAIN_HANDLE = LOGGER_CONTROL.getLogger()
    LOGGER_MAIN_HANDLE.info(G_parameter)

    rest_api = api_calls(G_parameter = G_parameter, loghandle = LOGGER_MAIN_HANDLE)
    jama_itemtypes = rest_api.getResource(resource="itemtypes", suffix="", params={"startAt":0,"maxResults":50}, \
                                              callback=data_reshape.getItemTypes_reshape, endless=True)

    project = 20393
    print(jama_itemtypes)
    jamadata = JamaData(project, jama_itemtypes, G_parameter, LOGGER_MAIN_HANDLE)
    allfeatures = jamadata.Get_allfeatuers()
    allrequirements = jamadata.Get_allrequirements()
    etl = ETL(allfeatures, allrequirements, project)
    feature_defect, defect_feature = etl.ETL_output()
    #LOGGER_MAIN_HANDLE.info(feature_defect)
    #LOGGER_MAIN_HANDLE.info(defect_feature)

    word = Word(Text, feature_defect, defect_feature, LOGGER_MAIN_HANDLE)
    word.generate_word()
    word.save()
