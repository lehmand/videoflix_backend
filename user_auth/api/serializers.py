from user_auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):

  password = serializers.CharField(write_only=True)
  repeated_password = serializers.CharField(write_only=True)
  
  class Meta:
    model = User
    fields = ['email', 'password', 'repeated_password']


  def validate(self, data):
    if data['password'] != data['repeated_password']:
      raise serializers.ValidationError({'password': ['Passwords dont match.']})
    if User.objects.filter(email=data['email']).exists():
      raise serializers.ValidationError({'email': ['Email is already in use.']})
    return data
  
  def create(self, validated_data):
    validated_data['username'] = validated_data['email']
    validated_data.pop('repeated_password')
    user = User.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user