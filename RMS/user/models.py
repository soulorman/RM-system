from django.db import models

class User(models.Model):
    name = models.CharField(max_length=32, null=False, default='')
    password = models.CharField(max_length=512, null=False, default='123')

    create_time = models.DateTimeField(null=False)

    # def as_dict(self):
    #     return {
    #         'id' : self.id,
    #         'name': self.name,
    #         'password': self.password,
    #         }

    def as_dict(self):
        rt = {}
        for k,v in self.__dict__.items():
            if isinstance(v, (int, float, bool, str)):
                rt[k] = v

        return rt