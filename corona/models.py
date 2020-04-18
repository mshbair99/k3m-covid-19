from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    pub_date = models.DateTimeField()

    def summary(self):
        return self.body[:100]

    def __str__(self):
        return self.title


class contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    messages = models.TextField()

    def __str__(self):
        return self.name