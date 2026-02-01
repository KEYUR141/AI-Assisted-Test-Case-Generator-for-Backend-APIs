from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class APISpecification(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    endpoint = models.CharField(max_length= 255)
    methods = ArrayField(models.CharField(max_length = 50))
    constraint = models.JSONField()
    headers = models.JSONField()


class RuleSet(models.Model):
    api_specs = models.ForeignKey(APISpecification, on_delete = models.CASCADE, related_name = 'rule_sets')
    name = models.CharField(max_length = 255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    rules = models.JSONField()


class TestGenerationRun(models.Model):
    api_specs = models.ForeignKey(APISpecification, on_delete = models.CASCADE, related_name = 'test_generation_runs')
    rule_set = models.ForeignKey(RuleSet, on_delete = models.CASCADE, related_name = 'test_generation_runs')
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    times_run = models.IntegerField(default = 0)
    STATUS_CHOICES = [
        ('not_executed', 'Not Executed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]
    status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default = 'not_executed')


class GeneratedTestCase(models.Model):
    test_generation_run = models.ForeignKey(TestGenerationRun, on_delete = models.CASCADE, related_name = 'generated_test_cases')
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    test_data = models.JSONField()
    expected_results = models.JSONField()
    reason = models.TextField()
    STATUS_CHOICES = [
        ('not_executed', 'Not Executed'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('error', 'Error'),
    ]
    status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default = 'not_executed')

class TestExecutionResult(models.Model):
    generated_test_case = models.ForeignKey(GeneratedTestCase, on_delete = models.CASCADE, related_name = 'test_execution_results')
    executed_at = models.DateTimeField(auto_now_add = True)
    STATUS_CHOICES = [
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('error', 'Error'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length = 50,choices = STATUS_CHOICES,default='pending')
    actual_results = models.JSONField()
    logs = models.JSONField()
    errors = models.JSONField()
