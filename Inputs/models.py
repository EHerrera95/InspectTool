from django.db import models

import xml.etree.ElementTree as ET
import os.path

#List of Criteria used in tool
criteria_list = [ 
    ('2015E_b1_Ambulatory', '2015E_b1_Ambulatory'),
    ('2015E_b1_Inpatient', '2015E_b1_Inpatient'),
    ('2015E_b6_Ambulatory', '2015E_b6_Ambulatory'),
    ('2015E_b6_Inpatient', '2015E_b6_Inpatient'),
    ('2015E_b7_Ambulatory', '2015E_b7_Ambulatory'),
    ('2015E_b7_Inpatient', '2015E_b7_Inpatient'),
    ('2015E_e1_Ambulatory', '2015E_e1_Ambulatory'),
    ('2015E_e1_Inpatient', '2015E_e1_Inpatient'),
    ('2015E_g9_Ambulatory', '2015E_g9_Ambulatory'),
    ('2015E_g9_Inpatient', '2015E_g9_Inpatient'),
]

# Defining a dictionary used as a reference to define in the final dictionary
# the section name of the LOINC code assigned based on criteria (For Results table purposes)
values_dict = {
    "51848-0" : "Assessment",
    "61146-7" : "Goals",
    "51847-2" : "Assessment and Plan",
    "75310-3" : "Health Concerns",
    "18776-5" : "Plan of Treatment",
    "42349-1" : "Reason for Referral",
    "47420-5" : "Functional Status",
    "10190-7" : "Cognitive Status",
    "8653-8" : "Discharge Instructions",
    "30954-2" : "Diagnostic Imaging",
}

# Table to hold information from Input Form
class InputModel(models.Model):
    criteria = models.CharField(max_length=64, choices=criteria_list) #choices are form list defined above
    filename = models.FileField(upload_to="media/") #Upload to project directory in media filepath

    def __str__(self):
        return f"{self.criteria} & {self.filename}"


class Validation():
    #Initialize all possible LOINC codes for later assignment based on Input Form
    assessment = "51848-0"
    goals = "61146-7"
    health_concerns = "75310-3"
    plan_of_treatment = "18776-5"
    assessment_and_plan = "51847-2"
    reason_for_referral = "42349-1"
    functional_status = "47420-5"
    cognitive_status = "10190-7"
    discharge_instruction = "8653-8"
    diagnostic_imaging = "30954-2"

    final_dict = {} #Store all data in nested dictionary, used to pass information to results page table
                    #Nested dictionary format: { LOINC_CODE :{ SECTION_NAME , NARRATIVE_TEXT_FOUND }}
    LOINC_List = []   #Store all LOINC codes assigned based on Input Form

    #Initialization class method called that 1) assigns the criteria selection and filepath from Input Form to class
    #2) then perform the assignVariables method based on criteria from form
    #3) finally perform Xpath Logic using all data
    def __init__(self, criteria, filepath):
        self.criteria = criteria
        self.filepath = filepath
        self.assignVariables(criteria)
        self.xpathLogic()

    # Based on criteria from input form -> Add needed LOINC CODES to LOINC_List
    def assignVariables(self, criteria):
        self.LOINC_List.clear()
        if self.criteria == "2015E_b1_Ambulatory":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.reason_for_referral)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)

        elif self.criteria == "2015E_b1_Inpatient":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.discharge_instruction)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)
        
        elif self.criteria == "2015E_b6_Ambulatory":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.reason_for_referral)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)

        elif self.criteria == "2015E_b6_Inpatient":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.discharge_instruction)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)
        
        elif self.criteria == "2015E_b7_Ambulatory":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.reason_for_referral)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)
       
        elif self.criteria == "2015E_b7_Inpatient":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.discharge_instruction)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)

        elif self.criteria == "2015E_e1_Ambulatory":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.reason_for_referral)
            self.LOINC_List.append(self.diagnostic_imaging)
       
        elif self.criteria == "2015E_e1_Inpatient":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.discharge_instruction)
            self.LOINC_List.append(self.diagnostic_imaging)

        elif self.criteria == "2015E_g9_Ambulatory":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.reason_for_referral)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)
       
        elif self.criteria == "2015E_g9_Inpatient":
            self.LOINC_List.append(self.assessment)
            self.LOINC_List.append(self.plan_of_treatment)
            self.LOINC_List.append(self.assessment_and_plan)
            self.LOINC_List.append(self.goals)
            self.LOINC_List.append(self.health_concerns)
            self.LOINC_List.append(self.discharge_instruction)
            self.LOINC_List.append(self.functional_status)
            self.LOINC_List.append(self.cognitive_status)
            
    # For All LOINC CODES assigned from Input form, if LOINC_List[i] is in look up list -> add found LOINC's to look up list
    def xpathLogic(self):

        #Local Variables
        code_list = []  #List that holds all LOINC codes found in the xpath of XML
        lu_list =[]     #Temporary Lookup List to concatenate all found text data into one single string 
        temp_dict = {}  #Child dictionary with LOINC codes and text lookup values ADDED to objects final dict

        #Initializations to use XPATH
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        namespace = {
            'cda' : 'urn:hl7-org:v3'
        }

        #1) Loop through all sections of XML & Add all LOINC codes found in XML to code_list
        for section in root.findall("cda:component/cda:structuredBody/cda:component/cda:section", namespace):
            for tag in section:
                if 'code' in tag.tag:
                    code = tag.get('code')
                    code_list.append(code)
    
        # For each new Visual Inspection, this clears all previous data to ensure a clean slate everytime
        self.final_dict.clear()
        
        # 2) For all LOINC codes assigned based on input criteria, compare to all LOINC codes found in XML
        #       -> if LOINC is in the document -> add LOINC and text found to final dictionary
        #       -> else -> add LOINC and text defaulted to 'Not Found'
        for LOINC in self.LOINC_List:
            temp = "" 
            temp_dict.clear
            i = values_dict.get(LOINC) #Reference dictionary to define section name & use i as key in final dictionary
            if LOINC in code_list:
                for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{LOINC}']..//", namespace):
                    lu_list.clear()
                    if (a.text != None and a.text != ""): #Checks within all regular tags for text data and store to lookup list
                        lu_list.append(a.text)
                    if(a.tail != None and a.tail != ""): #Checks in between regular tags (tail) for text data and store to lookup list
                        lu_list.append(a.tail)
                    for u in lu_list:
                        temp = temp + "  " + u + " "
                temp_dict["LOINC"]= LOINC
                temp_dict["txt"]= temp
            else:
                temp_dict["LOINC"]= "Not Found"
                temp_dict["txt"]= "Not Found"
            #Add either found or not found data to final dictionary
            self.final_dict[i]=temp_dict.copy()