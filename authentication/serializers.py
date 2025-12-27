from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()

# Serializer for user registration with detailed validations, including password strength
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm', 'first_name', 'last_name', 
                  'phone_number', 'city', 'state', 'country')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'country': {'required': False},
            'state': {'required': False},
            'city': {'required': False},
        }

    def validate(self, attrs):

        firstName = attrs['first_name']
        lastName = attrs['last_name']
          
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if len(firstName) < 2 or len(lastName) < 2:
            raise serializers.ValidationError("First_name and last_name must be at least 2 characters long.")
        
        if not any(char.isalpha() for char in firstName):
                raise serializers.ValidationError("firstname must contain characters.")
        
        if not any(char.isalpha() for char in lastName):
                raise serializers.ValidationError("lastname must contain characters.")
             
        if not attrs.get('first_name'):
            raise serializers.ValidationError({"first_name": "This field is required."})

        if not attrs.get('last_name'):
            raise serializers.ValidationError({"last_name": "This field is required."})
        
        if not attrs.get('phone_number'):
            raise serializers.ValidationError({"phone_number": "This field is required."})
        
        
        # field validation list
        password = attrs['password']
        
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})

        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError({"password": "Password must contain both letters and numbers."})

        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least one special character."})

        if password.lower() in ['password', '12345678', 'qwert123', 'letmein', 'welcome']:
            raise serializers.ValidationError({"password": "Password is too common."})

        if ' ' in password:
            raise serializers.ValidationError({"password": "Password should not contain spaces."})

        if password.islower() or password.isupper():
            raise serializers.ValidationError({"password": "Password must contain both uppercase and lowercase letters."})
        
        email_prefix = attrs['email'].split('@')[0]
        if len(email_prefix) >= 3 and email_prefix.lower() in password.lower():
            raise serializers.ValidationError({"password": "Password should not contain parts of your email."})
        

        return attrs
        

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value
        

    # Create user instance with validated data
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm', None)

        # Create the user
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user


# Login serializer for user authentication, checking email and password fields if provided and valid
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username')
        read_only_fields = ('id', 'expires_at')


# User serializer for retrieving user details after authentication if the user is authenticated and exists
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff')
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'address', 'city', 
                  'state', 'country', 'postal_code', 'date_of_birth')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    new_password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    new_password_confirm = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")

        return value

    def validate(self, attrs):
    # Ensure both fields exist before comparing
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

    # Cross-field validation
        if new_password != new_password_confirm:
            raise serializers.ValidationError({
            "new_password_confirm": "Passwords do not match."
        })

        # Validate password strength
        user = self.context['request'].user
        validate_password(new_password, user=user)

        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
            
        return attrs
    


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()