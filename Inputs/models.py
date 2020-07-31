from django.db import models

criteria_list = [ 
    ('2015E_b1_Amb_Sample1_CCD', '2015E_b1_Amb_Sample1_CCD'),
    ('2015E_b1_Amb_Sample1_RN', '2015E_b1_Amb_Sample1_RN'),
    ('2015E_b1_Amb_Sample2_CCD', '2015E_b1_Amb_Sample2_CCD'),
    ('2015E_b1_Amb_Sample2_RN','2015E_b1_Amb_Sample2_RN')
]

passfail_list = [
    ('PASS', 'PASS'),
    ('FAIL - CHECK CONTENTS OF XML', 'FAIL - CHECK CONTENTS OF XML'),
    ('Not Tested', 'Not Tested')
]

# Create your models here.
class InputModel(models.Model):
    criteria = models.CharField(max_length=64, choices=criteria_list)
    filename = models.FileField(upload_to="media/")

    def __str__(self):
        return f"{self.criteria} & {self.filename}"


class VariableSet(models.Model):
    assessment = models.CharField(max_length=64, null=True, blank=True)
    assessment_txt = models.CharField(max_length=128, null=True, blank=True) 
    goals = models.CharField(max_length=64, null=True, blank=True)
    goals_txt = models.CharField(max_length=128, null=True, blank=True)
    health_concerns = models.CharField(max_length=64, null=True, blank=True)
    health_concerns_txt = models.CharField(max_length=128, null=True, blank=True)
    plan_of_treatment = models.CharField(max_length=64, null=True, blank=True)
    plan_of_treatment_txt = models.CharField(max_length=128, null=True, blank=True)
    reason_for_referral = models.CharField(max_length=64, null=True, blank=True)
    reason_for_referral_txt = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.assessment} | {self.assessment_txt} | {self.goals} | {self.goals_txt} | {self.health_concerns} | {self.health_concerns_txt}| {self.plan_of_treatment}| {self.plan_of_treatment_txt} | {self.reason_for_referral} | {self.reason_for_referral_txt}"


class ResultSet(models.Model):
    assessment_results = models.CharField(max_length=32, choices=passfail_list, default="")
    assessment_txt_results = models.CharField(max_length=32, choices=passfail_list, default="")
    goals_results = models.CharField(max_length=32, choices=passfail_list, default="")
    goals_txt_results = models.CharField(max_length=32, choices=passfail_list, default="")
    health_concerns_results = models.CharField(max_length=32, choices=passfail_list, default="")
    health_concerns_txt_results = models.CharField(max_length=32, choices=passfail_list, default="")
    plan_of_treatment_results = models.CharField(max_length=32, choices=passfail_list, default="")
    plan_of_treatment_txt_results = models.CharField(max_length=32, choices=passfail_list, default="")
    reason_for_referral_results = models.CharField(max_length=32, choices=passfail_list, default="")
    reason_for_referral_txt_results = models.CharField(max_length=32, choices=passfail_list, default="")

    def __str__(self):
        return f"{self.assessment_results} | {self.assessment_txt_results} | {self.goals_results} | {self.goals_txt_results} | {self.health_concerns_results} | {self.health_concerns_txt_results}  | {self.plan_of_treatment_results} | {self.plan_of_treatment_txt_results} | {self.reason_for_referral_results} | {self.reason_for_referral_txt_results}"