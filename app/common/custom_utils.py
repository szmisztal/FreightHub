import os
import logging
from marshmallow import ValidationError

def create_logger(app, log_folder, log_file_name):
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_path = os.path.join(log_folder, log_file_name)

    handler = logging.FileHandler(log_path)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

def not_blank(value):
    if not value:
        raise ValidationError("Field may not be null.")

def send_validation_errors_to_form(errors, form):
    for field_name, messages in errors.messages.items():
        field = getattr(form, field_name)
        if isinstance(field.errors, list):
            field.errors.extend(messages)
        else:
            field.errors = list(messages)
