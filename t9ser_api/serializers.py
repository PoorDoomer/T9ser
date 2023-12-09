from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from t9ser_api.models import Sport,Match,UserMatch


class SportSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Sport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class MatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sport = serializers.PrimaryKeyRelatedField(queryset=Sport.objects.all())
    host_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    location = serializers.CharField(style={'base_template': 'textarea.html'})
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    players_needed = serializers.IntegerField()
    date_time = serializers.DateTimeField()
    created_at = serializers.DateTimeField(read_only=True)
    name = serializers.SerializerMethodField()
    def get_name(self, obj):
        # Assuming host_user is a ForeignKey to a User model that has a field 'username'
        host_username = obj.host_user.username if obj.host_user else 'Unknown'
        # Formatting the date_time to a readable format
        date_time_str = obj.date_time.strftime('%Y-%m-%d %H:%M') if obj.date_time else 'Unknown'
        # Concatenating the fields
        return f"{obj.location} hosted by {host_username} at {date_time_str}"

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sport = validated_data.get('sport', instance.sport)
        instance.host_user = validated_data.get('host_user', instance.host_user)
        instance.location = validated_data.get('location', instance.location)
        instance.price = validated_data.get('price', instance.price)
        instance.players_needed = validated_data.get('players_needed', instance.players_needed)
        instance.date_time = validated_data.get('date_time', instance.date_time)
        instance.save()
        return instance


class UserMatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())
    is_approved = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return UserMatch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.match = validated_data.get('match', instance.match)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


