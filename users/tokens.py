from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Генератор токенов для подтверждения email при регистрации пользователя.
    Наследует механизм генерации токенов сброса пароля.
    """
    pass


# Экземпляр генератора токенов для активации аккаунта по email
account_activation_token = EmailVerificationTokenGenerator()
