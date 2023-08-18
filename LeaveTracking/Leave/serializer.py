from rest_framework import serializers
from .models import Employee_Detail, Leave

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Detail
        fields = '__all__'

    def create(self, validated_data):
        return Employee_Detail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Employee_Name = validated_data.get('Employee_Name', instance.Employee_Name)
        instance.password = validated_data.get('password', instance.password)
        instance.Primary_Phone = validated_data.get('Primary_Phone', instance.Primary_Phone)  # Corrected attribute name
        instance.Email = validated_data.get('Email', instance.Email)
        instance.save()
        return instance


class LeaveSerializer(serializers.ModelSerializer):
    empname = EmployeeSerializer(many=True, read_only=True)
    class Meta:
        model = Leave
        fields = '__all__'

    def create(self, validated_data):
        return Leave.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Employee_Name = validated_data.get('Employee_Name', instance.Employee_Name)
        instance.Month = validated_data.get('Month', instance.Month)
        instance.Year = validated_data.get('Year', instance.Year)
        instance.Start_Date = validated_data.get('Start_Date', instance.Start_Date)
        instance.End_Date = validated_data.get('End_Date',instance.End_Date)
        instance.Reason = validated_data.get('Reason', instance.Reason)
        instance.Status = validated_data.get('Status', instance.Status)
        instance.save()
        return instance