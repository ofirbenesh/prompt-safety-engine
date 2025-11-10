from app.redactors.email_redactor import EmailRedactor
from app.redactors.phone_redactor import PhoneRedactor
from app.redactors.secret_redactor import SecretRedactor
from app.redactors.credit_card_redactor import CreditCardRedactor

def get_all_redactors():
    return [
        EmailRedactor(),
        CreditCardRedactor(),
        PhoneRedactor(),
        SecretRedactor(),
    ]