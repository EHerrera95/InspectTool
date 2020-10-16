from django.shortcuts import redirect, render, reverse

from .forms import InputForm
from .models import InputModel, VariableSet, LookupSet
from django.core.files.storage import FileSystemStorage


import xml.etree.ElementTree as ET
import os.path

#--------------------------------------------------------------------------------------------------------------------
#               Issues to be fixed
#1) Edit Results Table to Output text found in the XML , no more PASS/FAIL
#   - 
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
    l = LookupSet.objects.all()

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
        'lookup' : l
    })


#Set appropriate variables based on criteria selected by proctor
def defineVars(crit):
    VariableSet.objects.all().delete()
    if crit == "2015E_b1_Amb_Sample1_CCD" or crit == "2015E_b1_Amb_Sample1_RN" or crit == "2015E_b1_Amb_Sample2_CCD" or  crit == "2015E_b1_Amb_Sample2_RN":
        if crit == "2015E_b1_Amb_Sample1_RN" or crit =="2015E_b1_Amb_Sample2_RN":
            reason_for_referral = "42349-1"
        else:
            reason_for_referral = "N/A"
        v = VariableSet(assessment = '51848-0', goals = '61146-7', plan_of_treatment="18776-5", health_concerns="75310-3",reason_for_referral = reason_for_referral, functional_status="47420-5", cognitive_status="10190-7")
        v.save()
    else:
        print("ERROR")


#Start Valiadtion
def startvalidation(v, filepath):
    #Start of XPath code
    tree = ET.parse(filepath)
    root = tree.getroot()

    namespace = {
        'cda' : 'urn:hl7-org:v3'
    }

    lu_list = []
    code_list = []
    assessment_lu="Not Found"
    assessment_txt_lu="Not Found"
    goals_lu="Not Found"
    goals_txt_lu="Not Found"
    health_concerns_lu="Not Found"
    health_concerns_txt_lu="Not Found"
    plan_of_treatment_lu="Not Found"
    plan_of_treatment_txt_lu="Not Found"
    reason_for_referral_lu="Not Found"
    reason_for_referral_txt_lu="Not Found"
    functional_status_lu="Not Found"
    functional_status_txt_lu="Not Found"
    cognitive_status_lu="Not Found"
    cognitive_status_txt_lu="Not Found"

    #1) Add all codes found in xml to code_list
    for section in root.findall("cda:component/cda:structuredBody/cda:component/cda:section", namespace):
        #print(section)
        for tag in section:
            #print(title.tag)
            if 'code' in tag.tag:
                code = tag.get('code')
                code_list.append(code)

    temp = ""    
    #2) Assessment
    if v[0].assessment in code_list:
        #Correct Assessment OID was found -> Output OID found
        assessment_lu=v[0].assessment

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].assessment}']../cda:text//", namespace):
            lu_list.clear()
            if (a.text != None and a.text != ""):
                lu_list.append(a.text)

            for u in lu_list:
                temp = temp + "  " + u + " |"
            assessment_txt_lu=temp

    temp = ""
    #3) Goals 
    if v[0].goals in code_list:
        #Correct Goals OID was found -> Output OID found
        goals_lu=v[0].goals

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].goals}']../cda:text//", namespace):
            lu_list.clear()
            if (a.text != None and a.text != ""):
                lu_list.append(a.text)

            for u in lu_list:
                temp = temp + "  " + u + " |"
            goals_txt_lu = temp


    temp = ""
    #4) Health Concerns 
    if v[0].health_concerns in code_list:
        #Correct Health Concerns OID was found -> Output OID found
        health_concerns_lu=v[0].health_concerns

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].health_concerns}']../cda:text//", namespace):
            lu_list.clear()
            if (a.text != None and a.text != ""):
                lu_list.append(a.text)

            for u in lu_list:
                temp = temp + "  " + u + " |"
            health_concerns_txt_lu = temp



    temp = ""
    #5) Plan of Treatment
    if v[0].plan_of_treatment in code_list:
        #Correct Plan of Treatment OID was found -> Output OID found
        plan_of_treatment_lu=v[0].plan_of_treatment

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].plan_of_treatment}']../cda:text//", namespace):
            lu_list.clear()
            if (a.text != None and a.text != ""):
                lu_list.append(a.text)

            for u in lu_list:
                temp = temp + "  " + u + " |"
            plan_of_treatment_txt_lu = temp

    temp = ""
    #6) Reason for Referral (Not Required for CCDS)
    # if v[0].reason_for_referral == "N/A":
    #     reason_for_referral_lu= "N/A"
    #     reason_for_referral_txt_lu= "N/A"

    if v[0].reason_for_referral in code_list:
        #Correct Reason for Referral OID was found -> Output OID found
        reason_for_referral_lu=v[0].reason_for_referral

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].reason_for_referral}']../cda:text//", namespace):
            lu_list.clear()
            if (a.text != None and a.text != ""):
                lu_list.append(a.text)

            for u in lu_list:
                temp = temp + "  " + u + " |"
            reason_for_referral_txt_lu = temp
    else:
        print("TO BE CODED")    

    temp = ""
    #7) Functional Status
    if v[0].functional_status in code_list:
        #Correct Functional Status OID was found -> Output OID found
        functional_status_lu=v[0].functional_status

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].functional_status}']../cda:text//", namespace):
            lu_list.clear()
            if (a.text != None and a.text != ""):
                lu_list.append(a.text)

            for u in lu_list:
                temp = temp + "  " + u + " |"
            functional_status_txt_lu = temp
    else:
        print("TO BE CODED")   

    temp = ""
    #8) Cognitive Status
    if v[0].cognitive_status in code_list:
        #Correct Cognitive Status OID was found -> Output OID found
        cognitive_status_lu=v[0].cognitive_status

        for a in root.findall(f"cda:component/cda:structuredBody/cda:component/cda:section/cda:code[@code='{v[0].cognitive_status}']../cda:text//", namespace):
            lu_list.clear()
            if (a.text != None and a.text != ""):
                lu_list.append(a.text)

            for u in lu_list:
                temp = temp + "  " + u + " |"
            cognitive_status_txt_lu = temp
    else:
        print("TO BE CODED")  

    LookupSet.objects.all().delete()
    l = LookupSet(assessment_lu=assessment_lu, assessment_txt_lu=assessment_txt_lu,goals_lu=goals_lu,goals_txt_lu=goals_txt_lu, health_concerns_lu=health_concerns_lu,health_concerns_txt_lu=health_concerns_txt_lu, plan_of_treatment_lu=plan_of_treatment_lu, plan_of_treatment_txt_lu=plan_of_treatment_txt_lu,reason_for_referral_lu=reason_for_referral_lu,reason_for_referral_txt_lu=reason_for_referral_txt_lu, functional_status_lu=functional_status_lu,functional_status_txt_lu=functional_status_txt_lu,cognitive_status_lu=cognitive_status_lu, cognitive_status_txt_lu=cognitive_status_txt_lu)
    l.save()
