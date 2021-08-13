from rest_framework import serializers


from profiles_api import models

from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','firstName','lastName','birthDay','gender','password')
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
                }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        print(f"here {validated_data['birthDay']}")
        user  = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            birthDay = validated_data['birthDay'],
            gender = validated_data['gender'],
            password = validated_data['password']
        )

        return user


class LoginSerializer(AuthTokenSerializer):
    """serializes a user profile object"""
    user = models.UserProfile

    class Meta:
        model = models.UserProfile
        fields = ('id','email','firstName','lastName','birthDay','gender')


class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceInfo
        fields = ('uuid', 'app_name', 'app_version', 'build_number',  'fcm_token', 'os_version', 'os', 'brand', 'model',
                  'user', 'id')

        extra_kwargs = {'user': {'read_only': True},
                        'id': {'read_only': True}}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = UserProfileSerializer().to_representation(models.UserProfile.objects.get(pk=ret['user']))
        return ret
