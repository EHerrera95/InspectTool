from django.db import models

criteria_list = [ 
    ('2015E_b1_Amb_Sample1_CCD', '2015E_b1_Amb_Sample1_CCD'),
    ('2015E_b1_Amb_Sample1_RN', '2015E_b1_Amb_Sample1_RN'),
    ('2015E_b1_Amb_Sample2_CCD', '2015E_b1_Amb_Sample2_CCD'),
    ('2015E_b1_Amb_Sample2_RN','2015E_b1_Amb_Sample2_RN')
]

# Create your models here.
class InputModel(models.Model):
    criteria = models.CharField(max_length=64, choices=criteria_list)
    filename = models.FileField(upload_to="media/")

    def __str__(self):
        return f"{self.criteria} & {self.filename}"


class VariableSet(models.Model):
    assessment = models.CharField(max_length=64, null=True, blank=True)
    goals = models.CharField(max_length=64, null=True, blank=True)
    health_concerns = models.CharField(max_length=64, null=True, blank=True)
    plan_of_treatment = models.CharField(max_length=64, null=True, blank=True)
    reason_for_referral = models.CharField(max_length=64, null=True, blank=True)
    functional_status = models.CharField(max_length=64, null=True, blank=True)
    cognitive_status = models.CharField(max_length=64, null=True, blank=True)


    def __str__(self):
        return f"{self.assessment} | {self.goals} | {self.health_concerns} | {self.plan_of_treatment}| {self.reason_for_referral}| {self.functional_status}| {self.cognitive_status}"


class LookupSet(models.Model):
    assessment_lu = models.CharField(max_length=1000, default="")
    assessment_txt_lu = models.CharField(max_length=1000, default="")
    goals_lu = models.CharField(max_length=1000, default="")
    goals_txt_lu = models.CharField(max_length=1000, default="")
    health_concerns_lu = models.CharField(max_length=1000, default="")
    health_concerns_txt_lu = models.CharField(max_length=1000, default="")
    plan_of_treatment_lu = models.CharField(max_length=1000, default="")
    plan_of_treatment_txt_lu = models.CharField(max_length=1000, default="")
    reason_for_referral_lu = models.CharField(max_length=1000, default="")
    reason_for_referral_txt_lu = models.CharField(max_length=1000, default="")
    functional_status_lu= models.CharField(max_length=1000, default="")
    functional_status_txt_lu = models.CharField(max_length=1000, default="")
    cognitive_status_lu= models.CharField(max_length=1000, default="")
    cognitive_status_txt_lu = models.CharField(max_length=1000, default="")

    def __str__(self):
        return "Lookup values"