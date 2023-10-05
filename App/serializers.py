from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User 




class RegisterAPISerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('username is taken')

            if data['email']:
                if User.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError('Email is taken')

            return data 

    def create(self, validated_data):
        # print(validated_data)
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data







class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=80)
    password = serializers.CharField(max_length=80)




class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['colour_name']

class PersonSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()   # nested serializers 
    # color_info = serializers.SerializerMethodField()   # custom serializer 

    class Meta:
        model = Person 
        fields = '__all__'
        # depth = 1

    # def get_color_info(self, obj):
    #     color_obj = Color.objects.get(id=obj.color.id)
    #     return {'color_name': color_obj.colour_name, 'hex_code': '#000'}

    def validate(self, data):

        special_characters = '!@#$%^&*()_+?_=,<>/:'
        if any(c in special_characters for c in data['first_name']):
            raise serializers.ValidationError('First name cannot contain special char')
        if any(c in special_characters for c in data['last_name']):
            raise serializers.ValidationError('Last name cannot contain special char')

        if data['age'] < 18:
            raise serializers.ValidationError("age should be greater than 18")

        return data

    # def validate_age(self, data)



