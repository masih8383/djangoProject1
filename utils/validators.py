from django.core.validators import RegexValidator

class PhoneNumberValidator(RegexValidator):
    regex = r'^\+?98[0-9]{10}$'
    message= 'Enter a valid phone number'
    code = 'invalid phone number'



validate_phone_number=PhoneNumberValidator