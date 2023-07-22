from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateField("date published")
    pub_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    pub_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateField("date published")

    def __str__(self):
        return self.comment_text
    
class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)