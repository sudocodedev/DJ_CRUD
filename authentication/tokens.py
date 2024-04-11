from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """overidding _make_hash_value method in PasswordResetTokenGenerator class to include user status whether he/ she is active or not"""
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))

account_activation_token = AccountActivationTokenGenerator()