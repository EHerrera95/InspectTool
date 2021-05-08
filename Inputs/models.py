from django.db import models

import xml.etree.ElementTree as ET
import os.path

#List of Criteria used in tool
criteria_list = [ 
    ('2015E_b1_Ambulatory', '2015E_b1_Ambulatory'),
    ('2015E_b1_Inpatient', '2015E_b1_Inpatient'),
    ('2015E_b6_Ambulatory', '2015E_b6_Ambulatory'),
    ('2015E_b6_Inpatient', '2015E_b6_Inpatient'),
]

#Defining OIDs to look for in Tool
values_dict = {
    "51848-0" : "Assessment",
    "61146-7" : "Goals",
    "75310-3" : "Health Concerns",
    "18776-5" : "Plan of Treatment",
    "42349-1" : "Reason for Referral",
    "47420-5" : "Functional Status",
    "10190-7" : "Cognitive Status",
    "8653-8" : "Discharge Instructions"
}

# Create your models here.

# Table to hold information from Input Menu
class InputModel(models.Model):
    criteria = models.CharField(max_length=64, choices=criteria_list)
    filename = models.FileField(upload_to="media/")

    def __str__(self):
        return f"{self.criteria} & {self.filename}"


class Validation():
    #Initialize all OIDs so object can assign whichever ones it needs
    assessment = "51848-0"
    goals = "61146-7"
    health_concerns = "75310-3"
    plan_of_treatment = "18776-5"
    reason_for_referral = "42349-1"
    functional_status = "47420-5"
    cognitive_status = "10190-7"
    discharge_instruction = "8653-8"
    final_dict = {}
    OID_List = []

    def __init__(self, criteria, filepath):
        self.criteria = criteria
        self.filepath = filepath
        self.assignVariables(criteria)
        self.xpathLogic()

    # Based on criteria -> Add needed OIDs to OID_List
    def assignVariables(self, criteria):
        self.OID_List.clear()
        if self.criteria == "2015E_b1_Ambulatory":
            self.OID_List.append(self.assessment)
            self.OID_List.append(self.plan_of_treatment)
            self.OID_List.append(self.goals)
            self.OID_List.append(self.health_concerns)
            self.OID_List.append(self.reason_for_referral)
            self.OID_List.append(self.functional_status)
            self.OID_List.append(self.cognitive_status)

        elif self.criteria == "2015E_b1_Inpatient":
            self.OID_List.append(self.assessment)
            self.OID_List.append(self.plan_of_treatment)
            self.OID_List.append(self.goals)
            self.OID_List.append(self.health_concerns)
            self.OID_List.append(self.discharge_instruction)
            self.OID_List.append(self.functional_status)
            self.OID_List.append(self.cognitive_status)
        
        elif self.criteria == "2015E_b6_Ambulatory":
            self.OID_List.append(self.assessment)
            self.OID_List.append(self.plan_of_treatment)
            self.OID_List.append(self.goals)
            self.OID_List.append(self.health_concerns)
            self.OID_List.append(self.reason_for_referral)
            self.OID_List.append(self.functional_status)
            self.OID_List.append(self.cognitive_status)

        elif self.criteria == "2015E_b6_Inpatient":
            self.OID_List.append(self.assessment)
            self.OID_List.append(self.plan_of_treatment)
            self.OID_List.append(self.goals)
            self.OID_List.append(self.health_concerns)
            self.OID_List.append(self.discharge_instruction)
            self.OID_List.append(self.functional_status)
            self.OID_List.append(self.cognitive_status)
            
    # For All in OID_list, if OID_List[i] is in look up list -> add found OID to look up list
    def xpathLogic(self):
        #Local Variables
        code_list = []  #To Store All OIDs found in the xpath of CCDA
        found_codes = [] 
        lu_list =[]     #Temporary Lookup List to be later concatenated into a single string 
        temp_dict = {} #child dictionary with OID and txt lookup values ADDED to objects final dict

        #Start of XPath code
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        namespace = {
            'cda' : 'urn:hl7-org:v3'
        }
        #1) Loop through all sections of XML & Add all OIDs found in XML to code_list
        for section in root.findall("cda:component/cda:structuredBody/cda:component/cda:section", namespace):
            for tag in section:
                if 'code' in tag.tag:
                    code = tag.get('code')
                    code_list.append(code)
    
        self.final_dict.clear()
        #2) For all OIDs assigned based on criteria 
        #       -> if OID is found w/XPATH -> add OID and txt to dictionary
        #       -> else -> set OID and txt to Not Found
        for OID in self.OID_List:
            temp = "" 
            temp_dict.clear
            i = values_dict.get(OID)
            if OID in code_list:
                found_codes.append(OID)
                for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{OID}']../cda:text//", namespace):
                    lu_list.clear()
                    if (a.text != None and a.text != ""):
                        lu_list.append(a.text)
                    for u in lu_list:
                        temp = temp + "  " + u + " "
                temp_dict["OID"]= OID
                temp_dict["txt"]= temp
            else:
                temp_dict["OID"]= "Not Found"
                temp_dict["txt"]= f"List of Codes found --->  {code_list}"
            self.final_dict[i]=temp_dict.copy()