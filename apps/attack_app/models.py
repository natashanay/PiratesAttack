from django.db import models
from apps.log_reg_attack_app.models import User

class HasAttacked(models.Model):
    attacker= models.ForeignKey(User, related_name="attack_list")
    defender= models.ForeignKey(User, related_name="defend_list")
    num_attacks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


