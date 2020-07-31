from django.shortcuts import redirect, render, reverse

from .forms import InputForm
from .models import InputModel, VariableSet, ResultSet
from django.core.files.storage import FileSystemStorage


import xml.etree.ElementTree as ET
import os.path

# This is an update to view.py

#--------------------------------------------------------------------------------------------------------------------
#               Issues to be fixed
#1)Health Concerns Sample1 : Capitalization issue w/  goals  s -> S difference
#2)Goals_txt, HC_txt & POT_txt for Sample 1
#3)Validation for 
#--------------------------------------------------------------------------------------------------------------------
#               Things to do
#1)Test on AWS servers
#2)Filepath is not xml document -> return "Upload right document"
#   - Don't upload file when not xml
#   - Delete file from server once complete?
#3)Edit home screen with instructions
#   - Last thing learn CSS to style webpage
#4)Export Results Table into .csv or other sort of file
#   - Proctors have report to download quickly
#5)Build out rest of criteria/Cures updates
#--------------------------------------------------------------------------------------------------------------------


# Create your views here.
def inputs(request):
    if request.method == 'POST':
        InputModel.objects.all().delete()
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('results')
    else:
        form = InputForm()
    return render(request, "Inputs/inputs.html", {
        'form':form,
    })

def results(request):
    uploads = InputModel.objects.all()
    v = VariableSet.objects.all()
    r = ResultSet.objects.all()

    crit = uploads[0].criteria

    path_string = uploads[0].filename
    text = str(path_string)
    file_type = text[-4:]
    if file_type != '.xml':
        print('ERROR')
        return redirect('inputs')    #Needs alert to import correct file
    else:
        filepath = f'.//media/{uploads[0].filename}'
        defineVars(crit)
        startvalidation(v, filepath)
    
    return render(request, "Inputs/results.html", {
        'uploads': uploads,
        'vars': v,
        'results': r
    })


def defineVars(crit):
    VariableSet.objects.all().delete()
    if crit == "2015E_b1_Amb_Sample1_CCD" or crit == "2015E_b1_Amb_Sample1_RN":
        if crit == "2015E_b1_Amb_Sample1_RN":
            reason_for_referral = "42349-1"
            reason_for_referral_txt = "Ms Alice Newman is being referred to Community Health Hospitals Inpatient facility because of the high fever noticed and suspected Anemia."
        else:
            reason_for_referral = "N/A"
            reason_for_referral_txt = "N/A"
        v = VariableSet(assessment = '51848-0', assessment_txt = "The patient was found to have fever and Dr Davis is suspecting Anemia based on the patient history. So Dr Davis asked the patient to closely monitor the temperature and blood pressure and get admitted to Community Health Hospitals if the fever does not subside within a day.", goals = '61146-7',goals_txt = "Get rid of intermittent fever that is occurring every few weeks. Need to gain more energy to do regular activities", health_concerns = '75310-3',health_concerns_txt = "a. Chronic Sickness exhibited by patient. HealthCare Concerns refer to underlying clinical facts i. Documented HyperTension problem ii. Documented HypoThyroidism problem iii. Watch Weight of patient", plan_of_treatment = '18776-5' ,plan_of_treatment_txt = "i. Get an EKG done on 6/23/2015. ii. Get a Chest X-ray done on 6/23/2015 showing the Lower Respiratory Tract Structure. iii. Take Clindamycin 300mg three times a day as needed if pain does not subside iv. Schedule follow on visit with Neighborhood Physicians Practice on 7/1/2015.", reason_for_referral = reason_for_referral, reason_for_referral_txt = reason_for_referral_txt )
        v.save()
    elif crit == "2015E_b1_Amb_Sample2_CCD" or  crit == "2015E_b1_Amb_Sample2_RN":
        if crit == "2015E_b1_Amb_Sample2_RN":
            reason_for_referral = "42349-1"
            reason_for_referral_txt = "N/A"
        else:
            reason_for_referral = "N/A"
            reason_for_referral_txt = "N/A"
        v = VariableSet(assessment = '51848-0', assessment_txt = "The patient was found to be healthy and advised to follow his current routine of exercise, work, sleep and quality of life.", goals = '61146-7',goals_txt = "N/A", health_concerns = '75310-3',health_concerns_txt = "N/A", plan_of_treatment = '18776-5' ,plan_of_treatment_txt = "Schedule a visit for next year", reason_for_referral = reason_for_referral, reason_for_referral_txt = reason_for_referral_txt )
        v.save()
    else:
        print("ERROR")


def startvalidation(v, filepath):
    #Start of XPath code
    tree = ET.parse(filepath)
    root = tree.getroot()

    namespace = {
        'cda' : 'urn:hl7-org:v3'
    }

    code_list = []

    #Add all codes found in xml to code_list
    for section in root.findall("cda:component/cda:structuredBody/cda:component/cda:section", namespace):
        #print(section)
        for tag in section:
            #print(title.tag)
            if 'code' in tag.tag:
                code = tag.get('code')
                code_list.append(code)

                            
    #Assessment
    if v[0].assessment in code_list:
        assessment_results='PASS'
        assessment_txt_results='FAIL - CHECK CONTENTS OF XML'

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].assessment}']../cda:text/cda:list//cda:paragraph//", namespace):
            if v[0].assessment_txt in (a.text or a.tail):
                assessment_txt_results='PASS'
    else:
        assessment_results='FAIL - CHECK CONTENTS OF XML'
        assessment_txt_results='FAIL - CHECK CONTENTS OF XML'

    #Goals 
    goals2_lst = []
    goals2 = ["Get rid of intermittent fever that is occurring every few weeks", "Need to gain more energy to do regular activities"]

    if v[0].goals in code_list:
        goals_results='PASS'
        if v[0].goals_txt == "N/A":
            goals_txt_results='NOT TESTED'
        else:
            for b in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].goals}']../cda:text//cda:paragraph", namespace):
                goals2_lst.append(b.text)
            for x in goals2:
                if x not in goals2_lst:
                    goals_txt_results='FAIL - CHECK CONTENTS OF XML'
                elif x in goals2_lst:
                    goals_txt_results='PASS'
    else:
        if v[0].goals_txt == "N/A":
            goals_txt_results='NOT TESTED'
            goals_results="FAIL - CHECK CONTENTS OF XML"
        else:
            goals_results='FAIL - CHECK CONTENTS OF XML'
            goals_txt_results='FAIL - CHECK CONTENTS OF XML'

    #Health Concerns
    hc_lst = []
    hc_txt_lst =['Chronic Sickness exhibited by patient','HealthCare Concerns refer to underlying clinical facts', 'Documented HyperTension problem', 'Documented HypoThyroidism problem', 'Watch Weight of patient' ]

    if v[0].health_concerns in code_list:
        health_concerns_results='PASS'
        health_concerns_txt_results='FAIL - CHECK CONTENTS OF XML'
        if v[0].health_concerns_txt == "N/A":
            health_concerns_txt_results='NOT TESTED'
        else:
            for c in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].health_concerns}']../cda:text//cda:td", namespace):
                #print(c.text)
                hc_lst.append(c.text)
                #health_concerns_txt_results='PASS'
            #print(hc_lst)
            #print(hc_txt_lst)
            for y in hc_lst:
                if y in hc_txt_lst:
                    health_concerns_txt_results='PASS'
                elif y not in hc_txt_lst:
                    health_concerns_txt_results='FAIL - CHECK CONTENTS OF XML'
        
        #health_concerns_txt_results='Not Tested'
    else:
        health_concerns_results='FAIL - CHECK CONTENTS OF XML'
        health_concerns_txt_results='FAIL - CHECK CONTENTS OF XML'


    #Plan of Treatmenet OID
    if v[0].plan_of_treatment in code_list:
        plan_of_treatment_results='PASS'
        #for d in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].plan_of_treatment}']../cda:text//cda:br", namespace):
            #print(f"{d.text} + {d.tail}")
        plan_of_treatment_txt_results='NOT TESTED'
    else:
        plan_of_treatment_results='FAIL - CHECK CONTENTS OF XML'
        plan_of_treatment_txt_results='FAIL - CHECK CONTENTS OF XML'

    if v[0].reason_for_referral == "N/A":
        reason_for_referral_results='NOT TESTED'
        reason_for_referral_txt_results='NOT TESTED'
    elif v[0].reason_for_referral in code_list:
        reason_for_referral_results='PASS'
        if v[0].reason_for_referral_txt == "N/A":
            reason_for_referral_txt_results="NOT TESTED"
        else:
            for e in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].reason_for_referral}']../cda:text//cda:paragraph", namespace):
                if e.text in v[0].reason_for_referral_txt:
                    #print(e.text)
                    reason_for_referral_txt_results='PASS'
    else:
        reason_for_referral_results='FAIL - CHECK CONTENTS OF XML'        
        reason_for_referral_txt_results='FAIL - CHECK CONTENTS OF XML'


    
    ResultSet.objects.all().delete()
    r = ResultSet(assessment_results=assessment_results, assessment_txt_results=assessment_txt_results, goals_results=goals_results, goals_txt_results=goals_txt_results,health_concerns_results=health_concerns_results, health_concerns_txt_results=health_concerns_txt_results,plan_of_treatment_results=plan_of_treatment_results, plan_of_treatment_txt_results=plan_of_treatment_txt_results,reason_for_referral_results=reason_for_referral_results, reason_for_referral_txt_results=reason_for_referral_txt_results)
    r.save()

