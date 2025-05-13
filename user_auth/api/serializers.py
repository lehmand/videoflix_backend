from user_auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    This serializer handles the validation and creation of new user accounts.
    It validates email uniqueness, password length, and password matching.
    Upon successful validation, it creates a new User instance and generates
    an authentication token for the user.
    """

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
  
    class Meta:
        """
        Meta configuration for the serializer.
        
        Specifies the model to use and which fields should be included
        in the serialization/deserialization process.
        """
        model = User
        fields = ['email', 'password', 'repeated_password']


    def validate(self, data):
        """Validate the data provided for user registration."""
        required_fields = ['email', 'password', 'repeated_password']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({field: [f'{field} is required.']})

        if len(data['password']) < 6:
            raise serializers.ValidationError({'password': ['Password must be at least 6 characters long.']})
        
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': ['Passwords dont match.']})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': ['Email is already in use.']})
            
        return data
  
    def create(self, validated_data):
        """Create a new user instance with the validated data."""
        validated_data['username'] = validated_data['email']
        validated_data.pop('repeated_password')
        
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        
        return user