from django.db import models


class ReportableModel(models.Model):

    def get_report_information(self):
        return self.__class__.__name__+"/"+self.id.__str__()

    class Meta:
        abstract = True