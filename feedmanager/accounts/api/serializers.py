from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input-type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
        write_only_fields = ('password2',)

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'}
            )
        user.set_password(password)
        user.save()
        return user
