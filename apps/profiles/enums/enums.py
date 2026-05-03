from django.db import models


class GenderChoice(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say", "Prefer Not to Say"


class CompanySize(models.TextChoices):
    SMALL = "1-10", "1-10 Employees"
    MEDIUM = "11-50", "11-50 Employees"
    LARGE = "51-200", "51-200 Employees"
    XLARGE = "201-500", "201-500 Employees"
    ENTERPRISE = "500+", "500+ Employees"
