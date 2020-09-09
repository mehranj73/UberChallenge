from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()



class CreateUserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(max_length=40, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=40, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["id","username", "password1", "password2", "first_name", "last_name"]
        read_only_fields = ["id"]


    #OBJECT LEVEL VALIDATION
    def validate(self, data):
        print(data)
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match !")
        return data

    #Create after Validation
    def create(self, validated_data):
        data = {k:v for k,v in validated_data.items() if k not in ["password1", "password2"]}
        user = User.objects.create_user(**data)
        #password
        user.set_password(validated_data["password1"])
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['id'] = user.id
        token["username"] = user.username

        return token
