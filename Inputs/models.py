from django.db import models

import xml.etree.ElementTree as ET
import os.path

#List of Criteria used in tool
criteria_list = [
    # -----------b1 List-----------
    ('b.1 Amb: Sample 1 - 2015e', 'b.1 Amb: Sample 1 - 2015e'),
    ('b.1 Amb: Sample 2 - 2015e', 'b.1 Amb: Sample 2 - 2015e'),   
    # ('b.1 Amb: Sample 3 - 2015e', 'b.1 Amb: Sample 3 - 2015e'),
    ('b.1 Amb: Sample 1 - 2015e (Cures Update)', 'b.1 Amb: Sample 1 - 2015e (Cures Update)'),
    ('b.1 Amb: Sample 2 - 2015e (Cures Update)', 'b.1 Amb: Sample 2 - 2015e (Cures Update)'),
    ('b.1 Amb: Sample 3 - 2015e (Cures Update)', 'b.1 Amb: Sample 3 - 2015e (Cures Update)'),  

    ('b.1 Inp: Sample 1 - 2015e', 'b.1 Inp: Sample 1 - 2015e'),
    ('b.1 Inp: Sample 2 - 2015e', 'b.1 Inp: Sample 2 - 2015e'),
    # ('b.1 Inp: Sample 3 - 2015e', 'b.1 Inp: Sample 3 - 2015e'),
    ('b.1 Inp: Sample 1 - 2015e (Cures Update)', 'b.1 Inp: Sample 1 - 2015e (Cures Update)'),
    ('b.1 Inp: Sample 2 - 2015e (Cures Update)', 'b.1 Inp: Sample 2 - 2015e (Cures Update)'),
    ('b.1 Inp: Sample 3 - 2015e (Cures Update)', 'b.1 Inp: Sample 3 - 2015e (Cures Update)'),
    
    # -----------b2 List-----------
    ('b.2 Amb: Sample 1 - R1.1 CCD - 2015e (Cures Update)', 'b.2 Amb: Sample 1 - R1.1 CCD - 2015e (Cures Update)'),
    ('b.2 Amb: Sample 1 - R2.1 CCD - 2015e (Cures Update)', 'b.2 Amb: Sample 1 - R2.1 CCD - 2015e (Cures Update)'),
    ('b.2 Amb: Sample 1 - R2.1 RN - 2015e (Cures Update)', 'b.2 Amb: Sample 1 - R2.1 RN - 2015e (Cures Update)'),
    ('b.2 Inp: Sample 1 - R2.1 DS - 2015e (Cures Update)', 'b.2 Inp: Sample 1 - R2.1 DS - 2015e (Cures Update)'),
    
    # -----------b7 List-----------
    ('b.7 Amb: Sample 1 - 2015e', 'b.7 Amb: Sample 1 - 2015e'),
    ('b.7 Inp: Sample 1 - 2015e', 'b.7 Inp: Sample 1 - 2015e'),
    ('b.7 Amb: Sample 1 - 2015e (Cures Update)', 'b.7 Amb: Sample 1 - 2015e (Cures Update)'),
    ('b.7 Inp: Sample 1 - 2015e (Cures Update)', 'b.7 Inp: Sample 1 - 2015e (Cures Update)'),
    
    # -----------b9 List-----------
    ('b.9 Amb: Sample 1 - 2015e', 'b.9 Amb: Sample 1 - 2015e'),
    ('b.9 Inp: Sample 1 - 2015e', 'b.9 Inp: Sample 1 - 2015e'),
    ('b.9 Amb: Sample 1 - 2015e (Cures Update)', 'b.9 Amb: Sample 1 - 2015e (Cures Update)'),
    ('b.9 Inp: Sample 1 - 2015e (Cures Update)', 'b.9 Inp: Sample 1 - 2015e (Cures Update)'),

    # -----------e1 List-----------
    ('e.1 Amb: Sample 1 - 2015e', 'e.1 Amb: Sample 1 - 2015e'),
    ('e.1 Amb: Sample 2 - 2015e', 'e.1 Amb: Sample 2 - 2015e'),
    ('e.1 Amb: Sample 1 - 2015e (Cures Update)', 'e.1 Amb: Sample 1 - 2015e (Cures Update)'),
    ('e.1 Amb: Sample 2 - 2015e (Cures Update)', 'e.1 Amb: Sample 2 - 2015e (Cures Update)'),
    ('e.1 Amb: Sample 3 - 2015e (Cures Update)', 'e.1 Amb: Sample 3 - 2015e (Cures Update)'),

    ('e.1 Inp: Sample 1 - 2015e', 'e.1 Inp: Sample 1 - 2015e'),
    ('e.1 Inp: Sample 2 - 2015e', 'e.1 Inp: Sample 2 - 2015e'),
    ('e.1 Inp: Sample 1 - 2015e (Cures Update)', 'e.1 Inp: Sample 1 - 2015e (Cures Update)'),
    ('e.1 Inp: Sample 2 - 2015e (Cures Update)', 'e.1 Inp: Sample 2 - 2015e (Cures Update)'),
    ('e.1 Amb: Sample 3 - 2015e (Cures Update)', 'e.1 Inp: Sample 3 - 2015e (Cures Update)'),
    # -----------g9 List-----------
    ('g.9 Amb: Sample 1 - 2015e', 'g.9 Amb: Sample 1 - 2015e'),
    ('g.9 Amb: Sample 2 - 2015e', 'g.9 Amb: Sample 2 - 2015e'),
    ('g.9 Amb: Sample 1 - 2015e (Cures Update)', 'g.9 Amb: Sample 1 - 2015e (Cures Update)'),
    ('g.9 Amb: Sample 2 - 2015e (Cures Update)', 'g.9 Amb: Sample 2 - 2015e (Cures Update)'),
    ('g.9 Amb: Sample 3 - 2015e (Cures Update)', 'g.9 Amb: Sample 3 - 2015e (Cures Update)'),

    ('g.9 Inp: Sample 1 - 2015e', 'g.9 Inp: Sample 1 - 2015e'),
    ('g.9 Inp: Sample 2 - 2015e', 'g.9 Inp: Sample 2 - 2015e'),
    ('g.9 Inp: Sample 1 - 2015e (Cures Update)', 'g.9 Inp: Sample 1 - 2015e (Cures Update)'),
    ('g.9 Inp: Sample 2 - 2015e (Cures Update)', 'g.9 Inp: Sample 2 - 2015e (Cures Update)'),
    ('g.9 Amb: Sample 3 - 2015e (Cures Update)', 'g.9 Inp: Sample 3 - 2015e (Cures Update)'),
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
    "8653-8"  : "Discharge Instructions",
    "30954-2" : "Diagnostic Tests/Laboratory Data",
    "47519-4" : "History of Procedures",
    "11506-3" : "Progress Note",
    "10164-2" : "History of Present Illness",
    "34117-2" : "History and Physical Note",
    "11488-4" : "Consultation Note",
    "18842-5" : "Discharge Summary",
    "48765-2" : "Allergies",
    "10160-0" : "Medications",
    "11450-4" : "Problems",
    "11383-7" : "Health Status",
    "62387-6" : "Interventions",
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
    diagnostic_lab = "30954-2"
    procedures = "47519-4"
    progress_note = "11506-3"
    history_physical_note = "34117-2"
    consultation_note = "11488-4"
    discharge_summary = "18842-5"
    allergies = "48765-2"
    medications = "10160-0"
    problems = "11450-4"
    health_status = "11383-7"
    interventions = "62387-6"

    final_dict = {} #Store all data in nested dictionary, used to pass information to results page table
                    #Nested dictionary format: { LOINC_CODE :{ SECTION_NAME , NARRATIVE_TEXT_FOUND }}
    LOINC_List = []   #Store all LOINC codes assigned based on Input Form
    guide_list = []

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
        self.guide_list.clear()

        # ------------------------ b1 ------------------------
        #Good
        if self.criteria == "b.1 Amb: Sample 1 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Alice Newman is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")

        #Good
        elif self.criteria == "b.1 Amb: Sample 2 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule a visit for next year.")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("Assessment: The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life. | Plan: i. Schedule a visit for next year.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")

        #Only Cures??
        elif self.criteria == "b.1 Amb: Sample 3 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have a fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2020 | ii. Get a Chest X-ray done on 6/23/2020 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2020")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2020 | ii. Get a Chest X-ray done on 6/23/2020 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2020")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Happy Kid is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")

       #Good
        elif self.criteria == "b.1 Amb: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Alice Newman is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")
            self.LOINC_List.append(self.procedures)
            self.guide_list.append("Pacemaker is operating properly, and the breathlessness is due to high fever and anxiety.")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Ms. Alice Newman was tested for the Urinalysis macro panel, and the results have been found to be normal.")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Ms. Alice Newman seems to be developing high fever and hence we recommend her to get admitted to a nearby hospital using the provided referral.")

        #Good
        elif self.criteria == "b.1 Amb: Sample 2 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule a visit for next year.")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("Assessment: The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life. | Plan: i. Schedule a visit for next year.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.history_physical_note)
            self.guide_list.append("Dr. Albert Davis examined Mr. Jeremy Bates and found him to be healthy but advised him to cut down on smoking")

        #Only Cures??
        elif self.criteria == "b.1 Amb: Sample 3 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have a fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2020 | ii. Get a Chest X-ray done on 6/23/2020 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2020")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2020 | ii. Get a Chest X-ray done on 6/23/2020 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2020")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Happy Kid is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.consultation_note)
            self.guide_list.append("Dr. Albert Davis diagnosed Ms. Happy Kid to be suffering from Fever and suspected Pneumonia and recommended admission to the Community Health Hospitals. The note was recorded on 22nd June at 11:00 am ET")
        
        #Good
        elif self.criteria == "b.1 Inp: Sample 1 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Diet: Diabetic low salt diet | 2. Medications: Take prescribed medication as advised | 3. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | 4. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")
     
        #Good
        elif self.criteria == "b.1 Inp: Sample 2 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility. | 2. In case of fever, take Tylenol as advised in plan of treatment.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")

        #Only Cures??
        elif self.criteria == "b.1 Inp: Sample 3 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal to keep Body Temperature at 98-99 degrees Fahrenheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Watch Weight of patient | iii. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("a. Diet: Low salt diet | b. Medications: Take prescribed medications as advised. | c. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | d. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")

        #EPIC masks progress note different for Reb Larson, 
        elif self.criteria == "b.1 Inp: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Diet: Diabetic low salt diet | 2. Medications: Take prescribed medication as advised | 3. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | 4. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")
            self.LOINC_List.append(self.procedures)
            self.guide_list.append("Dr Seven examined Ms Rebecca Larson and found that the pacemaker is operating properly and the breathlessness is due to high fever and anxiety.")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Ms Rebecca Larson was tested for Urinanalysis macro panel and CBC and the results have been found to be normal.")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Ms Rebecca Larson got admitted due to developing high fever and since has shown considerable improvement and can be discharged shortly.")

        elif self.criteria == "b.1 Inp: Sample 2 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility. | 2. In case of fever, take Tylenol as advised in plan of treatment.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.discharge_summary)
            self.guide_list.append("Dr. Henry Seven after treating Mr John Wright for the burns has discharged Mr Wright to keep fever under control and visit back after a week.")

        #Epic masks ProgressNote and Lab in different LOINC
        elif self.criteria == "b.1 Inp: Sample 3 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal to keep Body Temperature at 98-99 degrees Fahrenheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Watch Weight of patient | iii. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("a. Diet: Low salt diet | b. Medications: Take prescribed medications as advised. | c. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | d. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Dr. Henry Seven after treating Ms. Jane Clarkson has seen considerable progress in her health in the two days that she was admitted to the hospital. The note was captured on June 24th 2020 at 11:00 am ET.")
            self.LOINC_List.append(self.discharge_summary)
            self.guide_list.append("Dr. Henry Seven has successfully discharged Ms. Jane Clarkson and has advised her to follow the diet recommendations. The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. The note was captured on June 24th 2020 at 11am ET.")


        # ------------------------ b2  ------------------------

        elif self.criteria == "b.2 Amb: Sample 1 - R1.1 CCD - 2015e (Cures Update)":
            self.LOINC_List.append(self.allergies)
            self.guide_list.append("Codeine | Aspirin")
            self.LOINC_List.append(self.medications)
            self.guide_list.append("0.09 MG/ACTUAT inhalant solution, 2 puffs")
            self.LOINC_List.append(self.problems)
            self.guide_list.append("Pneumonia | Asthma")

        elif self.criteria == "b.2 Amb: Sample 1 - R2.1 CCD - 2015e (Cures Update)":
            self.LOINC_List.append(self.allergies)
            self.guide_list.append("Penicillin G benzathine | Ampicillin Sodium")
            self.LOINC_List.append(self.medications)
            self.guide_list.append("Certiaxone 100 mg/mL | Aranesp 0.5 mg/mL | Tylenol 500mg")
            self.LOINC_List.append(self.problems)
            self.guide_list.append("Fever | Overweight | Essential hypertension | Severe Hypothroidism | Chronic rejection of renal transplant")

        elif self.criteria == "b.2 Amb: Sample 1 - R2.1 RN - 2015e (Cures Update)":
            self.LOINC_List.append(self.allergies)
            self.guide_list.append("Penicillin G benzathine | Ampicillin Sodium")
            self.LOINC_List.append(self.medications)
            self.guide_list.append("Certiaxone 100 mg/mL | Aranesp 0.5 mg/mL | Tylenol 500mg")
            self.LOINC_List.append(self.problems)
            self.guide_list.append("Fever | Overweight | Essential hypertension | Severe Hypothroidism | Chronic rejection of renal transplant")

        elif self.criteria == "b.2 Inp: Sample 1 - R2.1 DS - 2015e (Cures Update)":
            self.LOINC_List.append(self.allergies)
            self.guide_list.append("Penicillin G benzathine | Ampicillin Sodium")
            self.LOINC_List.append(self.medications)
            self.guide_list.append("Aranesp 0.5 mg/mL | Tylenol 500mg")
            self.LOINC_List.append(self.problems)
            self.guide_list.append("Essential hypertension | Iron deficiency anemia | Interstitial pneumonia | Overweight | Severe Hypothroidism | Chronic rejection of renal transplant")


        # ------------------------ b6  ------------------------

        # elif self.criteria == "b.6 Amb: Sample 1 - 2015e ":
        #     pass

        # ------------------------ b7 ------------------------
        #Need to update 2015e Cures with the lesser data elements??
        elif self.criteria == "b.7 Amb: Sample 1 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Alice Newman is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")
       
        elif self.criteria == "b.7 Inp: Sample 1 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Diet: Diabetic low salt diet | 2. Medications: Take prescribed medication as advised | 3. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | 4. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")

        elif self.criteria == "b.7 Amb: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
   
        elif self.criteria == "b.7 Inp: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Diet: Diabetic low salt diet | 2. Medications: Take prescribed medication as advised | 3. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | 4. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")


        # ------------------------ b9 ------------------------

        elif self.criteria == "b.9 Amb: Sample 1 - 2015e":
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a) Get rid of intermittent fever that is occurring every few weeks. b) Need to gain more energy to do regular activities. c)[Negotiated Goal for Body Temperature 6/22/15] d) Keep weight under 95kg.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            self.LOINC_List.append(self.health_status)
            self.guide_list.append("a) Outcome Observation #1: i. [Refers to Goal Observation for Weight] ii. [Refers to the Intervention Act #1] iii. [Progress Towards Goal of Weight - Goal Not Achieved as of 6/22/2015] | b) Outcome Observation #2: i. [Refers to Goal Observation for Body Temperature] ii. [Refers to Intervention Act #2] iii. [Progress Towards Goal of Body Temperature - Goal Achieved as of 6/24/2015")
            self.LOINC_List.append(self.interventions)
            self.guide_list.append("a) [Intervention Act #1:] i. Nutrition Recommendations: 1. Follow dietary regime as discussed, 182922004 - Dietary Regime (SNOMED-CT) 2. Read about nutrition as discussed, 61310001 - Nutrition Education procedure, (SNOMED-CT) iii. Refers to the Goal Observation for Body Temperature | b) [Intervention Act #2:] i. Refers to Medications entries. ii. Refers to Goal Observation for Body Temperature.")

        elif self.criteria == "b.9 Inp: Sample 1 - 2015e":
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a) Get rid of intermittent fever that is occurring every few weeks. b) Need to gain more energy to do regular activities. c)[Negotiated Goal for Body Temperature 6/22/15] d) Keep weight under 95kg.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Iron Defieciency Anemia problem concern")
            self.LOINC_List.append(self.health_status)
            self.guide_list.append("a) Outcome Observation #1: i. [Refers to Goal Observation for Weight] ii. [Refers to the Intervention Act #1] iii. [Progress Towards Goal of Weight - Goal Not Achieved as of 6/22/2015] | b) Outcome Observation #2: i. [Refers to Goal Observation for Body Temperature] ii. [Refers to Intervention Act #2] iii. [Progress Towards Goal of Body Temperature - Goal Achieved as of 6/24/2015")
            self.LOINC_List.append(self.interventions)
            self.guide_list.append("a) [Intervention Act #1:] i. Nutrition Recommendations: 1. Follow dietary regime as discussed, 182922004 - Dietary Regime (SNOMED-CT) 2. Read about nutrition as discussed, 61310001 - Nutrition Education procedure, (SNOMED-CT) iii. Refers to the Goal Observation for Body Temperature | b) [Intervention Act #2:] i. Refers to Medications entries. ii. Refers to Goal Observation for Body Temperature.")

        elif self.criteria == "b.9 Amb: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a) Get rid of intermittent fever that is occurring every few weeks. b) Need to gain more energy to do regular activities. c)[Negotiated Goal for Body Temperature 6/22/15] d) Keep weight under 95kg.")
            self.LOINC_List.append(self.health_status)
            self.guide_list.append("a) Outcome Observation #1: i. [Refers to Goal Observation for Weight] ii. [Refers to the Intervention Act #1] iii. [Progress Towards Goal of Weight - Goal Not Achieved as of 6/22/2015] | b) Outcome Observation #2: i. [Refers to Goal Observation for Body Temperature] ii. [Refers to Intervention Act #2] iii. [Progress Towards Goal of Body Temperature - Goal Achieved as of 6/24/2015")
            self.LOINC_List.append(self.interventions)
            self.guide_list.append("a) [Intervention Act #1:] i. Nutrition Recommendations: 1. Follow dietary regime as discussed, 182922004 - Dietary Regime (SNOMED-CT) 2. Read about nutrition as discussed, 61310001 - Nutrition Education procedure, (SNOMED-CT) iii. Refers to the Goal Observation for Body Temperature | b) [Intervention Act #2:] i. Refers to Medications entries. ii. Refers to Goal Observation for Body Temperature.")

        elif self.criteria == "b.9 Inp: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a) Get rid of intermittent fever that is occurring every few weeks. b) Need to gain more energy to do regular activities. c)[Negotiated Goal for Body Temperature 6/22/15] d) Keep weight under 95kg.")
            self.LOINC_List.append(self.health_status)
            self.guide_list.append("a) Outcome Observation #1: i. [Refers to Goal Observation for Weight] ii. [Refers to the Intervention Act #1] iii. [Progress Towards Goal of Weight - Goal Not Achieved as of 6/22/2015] | b) Outcome Observation #2: i. [Refers to Goal Observation for Body Temperature] ii. [Refers to Intervention Act #2] iii. [Progress Towards Goal of Body Temperature - Goal Achieved as of 6/24/2015")
            self.LOINC_List.append(self.interventions)
            self.guide_list.append("a) [Intervention Act #1:] i. Nutrition Recommendations: 1. Follow dietary regime as discussed, 182922004 - Dietary Regime (SNOMED-CT) 2. Read about nutrition as discussed, 61310001 - Nutrition Education procedure, (SNOMED-CT) iii. Refers to the Goal Observation for Body Temperature | b) [Intervention Act #2:] i. Refers to Medications entries. ii. Refers to Goal Observation for Body Temperature.")


        # ------------------------ e1 ------------------------

        elif self.criteria == "e.1 Amb: Sample 1 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Urinanalyis macro (dipstick) panel on 6/29/2015 | ii. Get an EKG done on 6/23/2015 | iii. Get a Chest X-ray done on 6/23/2015 | iv. Take Clindamycin 300mg three times a day as needed if pain does not subside. | v. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Urinanalyis macro (dipstick) panel on 6/29/2015  | ii. Get an EKG done on 6/23/2015 | iii. Get a Chest X-ray done on 6/23/2015 | iv. Take Clindamycin 300mg three times a day as needed if pain does not subside. | v. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)            
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Alice Newman is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")       
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Chest X-Rays: 2 Views on 6/23/15 - Lungs are not clear, cannot rule out Anemia. Other tests are required to determine the presence of Anemia.")

        elif self.criteria == "e.1 Amb: Sample 2 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule a visit for next year.")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("Assessment: The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life. | Plan: i. Schedule a visit for next year.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("No information")
        
        elif self.criteria == "e.1 Amb: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Urinanalyis macro (dipstick) panel on 6/29/2015 | ii. Get an EKG done on 6/23/2015 | iii. Get a Chest X-ray done on 6/23/2015 | iv. Take Clindamycin 300mg three times a day as needed if pain does not subside. | v. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Urinanalyis macro (dipstick) panel on 6/29/2015  | ii. Get an EKG done on 6/23/2015 | iii. Get a Chest X-ray done on 6/23/2015 | iv. Take Clindamycin 300mg three times a day as needed if pain does not subside. | v. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)            
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Alice Newman is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")            
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Chest X-Rays: 2 Views on 6/23/15 - Lungs are not clear, cannot rule out Anemia. Other tests are required to determine the presence of Anemia.")

        elif self.criteria == "e.1 Amb: Sample 2 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule a visit for next year.")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("Assessment: The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life. | Plan: i. Schedule a visit for next year.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.history_physical_note)
            self.guide_list.append("Dr. Albert Davis examined Mr. Jeremy Bates and found him to be healthy but advised him to cut down on smoking.")

        elif self.criteria == "e.1 Amb: Sample 3 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2020 | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2020")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2020 | ii. Get a Chest X-ray done on 6/23/2015 | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)            
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem")
            self.LOINC_List.append(self.reason_for_referral)
            self.guide_list.append("Ms. Happy Kid is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia.")
            self.LOINC_List.append(self.consultation_note)
            self.guide_list.append("Dr Albert Davis diagnosed Ms Happy Kid to be suffering from Fever and suspected Pneumonia and recommended admission to the Community Health Hospitals. The note was captured on June 22nd 2020 at 11:00 am ET.")

        elif self.criteria == "e.1 Inp: Sample 1 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Diet: Diabetic low salt diet | 2. Medications: Take prescribed medication as advised | 3. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | 4. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Chest X-Rays: 2 Views on 6/22/15 - Lungs are not clear, cannot rule out Anemia. Other tests are required to determine the presence of Anemia.")

        elif self.criteria == "e.1 Inp: Sample 2 - 2015e":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility. | 2. In case of fever, take Tylenol as advised in plan of treatment.")

        elif self.criteria == "e.1 Inp: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Diet: Diabetic low salt diet | 2. Medications: Take prescribed medication as advised | 3. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | 4. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("Functional Condition: Dependence on Cane | Date: 5/1/2005")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("Cognitive Status: Amnesia | Date: 5/1/2005")
            self.LOINC_List.append(self.procedures)
            self.guide_list.append("Dr Seven examined Ms Rebecca Larson and found that the pacemaker is operating properly and the breathlessness is due to high fever and anxiety.")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Ms Rebecca Larson was tested for Urinanalysis macro panel and CBC and the results have been found to be normal.")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Ms Rebecca Larson got admitted due to developing high fever and since has shown considerable improvement and can be discharged shortly.")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Chest X-Rays: 2 Views on 6/22/15 - Lungs are not clear, cannot rule out Anemia. Other tests are required to determine the presence of Anemia.")

        elif self.criteria == "e.1 Inp: Sample 2 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility. | 2. In case of fever, take Tylenol as advised in plan of treatment.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.discharge_summary)
            self.guide_list.append("Dr. Henry Seven after treating Mr John Wright for the burns has discharged Mr Wright to keep fever under control and visit back after a week.")

        elif self.criteria == "e.1 Inp: Sample 3 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal to keep Body Temperature at 98-99 degrees Fahrenheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Watch Weight of patient | iii. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("a. Diet: Low salt diet | b. Medications: Take prescribed medications as advised. | c. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | d. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.functional_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.cognitive_status)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Dr. Henry Seven after treating Ms. Jane Clarkson has seen considerable progress in her health in the two days that she was admitted to the hospital. The note was captured on June 24th 2020 at 11:00 am ET.")
            self.LOINC_List.append(self.discharge_summary)
            self.guide_list.append("Dr. Henry Seven has successfully discharged Ms. Jane Clarkson and has advised her to follow the diet recommendations. The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. The note was captured on June 24th 2020 at 11am ET.")

        # ------------------------ g9 ------------------------

        elif self.criteria == 'g.9 Amb: Sample 1 - 2015e':
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")            
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)            
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            
        elif self.criteria == 'g.9 Amb: Sample 2 - 2015e':
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule a visit for next year.")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("Assessment: The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life. | Plan: i. Schedule a visit for next year.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")

        elif self.criteria == "g.9 Amb: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2015 | ii. Get a Chest X-ray done on 6/23/2015 | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015")
            self.LOINC_List.append(self.goals)            
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient")
            self.LOINC_List.append(self.procedures)
            self.guide_list.append("Pacemaker is operating properly, and the breathlessness is due to high fever and anxiety.")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Ms. Alice Newman was tested for the Urinalysis macro panel, and the results have been found to be normal.")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Ms. Alice Newman seems to be developing high fever and hence we recommend her to get admitted to a nearby hospital using the provided referral.")
            
        elif self.criteria == "g.9 Amb: Sample 2 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule a visit for next year.")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("Assessment: The patient was found to be healthy and advised to follow his current routine of exercise, works, sleep, and quality of life. | Plan: i. Schedule a visit for next year.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.history_physical_note)
            self.guide_list.append("Dr. Albert Davis examined Mr. Jeremy Bates and found him to be healthy but advised him to cut down on smoking")

        elif self.criteria == "g.9 Amb: Sample 3 - 2015e (Cures Update)":
            self.guide_list.append("The patient was found to have a fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Get an EKG done on 6/23/2020 | ii. Get a Chest X-ray done on 6/23/2020 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2020")
            self.LOINC_List.append(self.assessment_and_plan)            
            self.guide_list.append("ASSESSMENT: The patient was found to have fever and Dr. Davis is suspecting Anemia based on the patient history. So, Dr. Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day. | PLAN: i. Get an EKG done on 6/23/2020 | ii. Get a Chest X-ray done on 6/23/2020 showing the Lower Respiratory Tract Structure. | iii. Take Clindamycin 300mg three times a day as needed if pain does not subside. | iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2020")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Get rid of intermittent fever that is occurring every few weeks. | b. Need to gain more energy to do regular activities.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem")
            self.LOINC_List.append(self.consultation_note)
            self.guide_list.append("Dr. Albert Davis diagnosed Ms. Happy Kid to be suffering from Fever and suspected Pneumonia and recommended admission to the Community Health Hospitals. The note was recorded on 22nd June at 11:00 am ET")

        elif self.criteria == 'g.9 Inp: Sample 1 - 2015e':
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")

        elif self.criteria == 'g.9 Inp: Sample 2 - 2015e':
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")

        elif self.criteria == "g.9 Inp: Sample 1 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Rebecca for Anemia during the 2 days stay at Community Health Hospitals. Ms. Rebecca recovered from Anemia during he stay and is being discharged in a stable condition. If there is a fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal for Body Temperature at 98-99 degrees Fahreinheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Chronic Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Documented Hypothyroidism problem | iii. Watch weight of patient | iv. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Diet: Diabetic low salt diet | 2. Medications: Take prescribed medication as advised | 3. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | 4. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.procedures)
            self.guide_list.append("Dr Seven examined Ms Rebecca Larson and found that the pacemaker is operating properly and the breathlessness is due to high fever and anxiety.")
            self.LOINC_List.append(self.diagnostic_lab)
            self.guide_list.append("Ms Rebecca Larson was tested for Urinanalysis macro panel and CBC and the results have been found to be normal.")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Ms Rebecca Larson got admitted due to developing high fever and since has shown considerable improvement and can be discharged shortly.")

        elif self.criteria == "g.9 Inp: Sample 2 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient Mr. John Wright was found to have first degree burns and Dr. Seven and his staff treated Mr. Wright by cleaning the burn and dressing the burn and observed for couple of hours before discharging Mr. Wright. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility. | ii. In case of high fever, take Tylenol as needed.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("No information")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("1. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility. | 2. In case of fever, take Tylenol as advised in plan of treatment.")
            self.LOINC_List.append(self.discharge_summary)
            self.guide_list.append("Dr. Henry Seven after treating Mr John Wright for the burns has discharged Mr Wright to keep fever under control and visit back after a week.")

        elif self.criteria == "g.9 Inp: Sample 3 - 2015e (Cures Update)":
            self.LOINC_List.append(self.assessment)
            self.guide_list.append("The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency.")
            self.LOINC_List.append(self.plan_of_treatment)
            self.guide_list.append("i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.assessment_and_plan)
            self.guide_list.append("ASSESSMENT: The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. | PLAN: i. Schedule an appointment with Dr. Seven after 1 week for Follow up with Outpatient facility for Immunosuppressive therapy.")
            self.LOINC_List.append(self.goals)
            self.guide_list.append("a. Need to gain more energy to do regular activities. | b. Negotiated Goal to keep Body Temperature at 98-99 degrees Fahrenheit with regular monitoring.")
            self.LOINC_List.append(self.health_concerns)
            self.guide_list.append("a. Sickness exhibited by patient | b. HealthCare Concerns refer to underlying clinical facts | i. Documented Hypertension problem | ii. Watch Weight of patient | iii. Documented Anemia problem")
            self.LOINC_List.append(self.discharge_instruction)
            self.guide_list.append("a. Diet: Low salt diet | b. Medications: Take prescribed medications as advised. | c. Appointments: Schedule an appointment with Dr. Seven after 1 week. Follow up with Outpatient facility for Immunosuppression treatment. | d. For Fever of > 101.5 F, or onset of chest pain/breathlessness contact Emergency.")
            self.LOINC_List.append(self.progress_note)
            self.guide_list.append("Dr. Henry Seven after treating Ms. Jane Clarkson has seen considerable progress in her health in the two days that she was admitted to the hospital. The note was captured on June 24th 2020 at 11:00 am ET.")
            self.LOINC_List.append(self.discharge_summary)
            self.guide_list.append("Dr. Henry Seven has successfully discharged Ms. Jane Clarkson and has advised her to follow the diet recommendations. The patient was found to have Anemia and Dr. Seven and his staff diagnosed the condition and treated Ms. Clarkson for Anemia during the 2 days stay at Community Health Hospitals. Ms. Clarkson recovered from Anemia during the stay and is being discharged in a stable condition. If there is fever greater than 101.5 F or onset of chest pain/breathlessness the patient is advised to contact emergency. The note was captured on June 24th 2020 at 11am ET.")

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
                temp_dict["txt"]= f"LOINCs found = {code_list}"
            #Add either found or not found data to final dictionary
            self.final_dict[i]=temp_dict.copy()
