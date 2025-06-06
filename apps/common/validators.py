from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import FileExtensionValidator, RegexValidator

validate_phone = RegexValidator(
    regex=r"^998\d{9}$",
    message="Phone number must begin with 998 and contain only 12 numbers",
    code="WRONG_PHONE_NUMBER",
)

image_common_extensions = FileExtensionValidator(
    allowed_extensions=("jpeg", "jpg", "png", "heic", "heif"),
    message="Wrong format uploaded image. Format must be: jpeg, jpg, png, heic or heif",  # noqa
    code="WRONG_IMAGE",
)

username_validator = UnicodeUsernameValidator()
