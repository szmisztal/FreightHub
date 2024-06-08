import os
import logging
from marshmallow import ValidationError

def create_logger(app, log_folder, log_file_name):
    """
    Create a logger for the Flask application.

    This function creates a logging handler that writes log messages to a file.
    It sets the log level to DEBUG and defines a log message format.

    Args:
        app (Flask): The Flask application instance.
        log_folder (str): The folder where the log file will be stored.
        log_file_name (str): The name of the log file.

    Returns:
        None
    """
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
    """
    Validate that a field is not blank.

    This function raises a ValidationError if the given value is None or empty.

    Args:
        value: The value to be validated.

    Raises:
        ValidationError: If the value is None or empty.

    Returns:
        None
    """
    if not value:
        raise ValidationError("Field may not be null.")

def send_validation_errors_to_form(errors, form):
    """
    Send validation errors to the form.

    This function takes validation errors from Marshmallow and adds them to the
    corresponding form fields' error lists.

    Args:
        errors (ValidationError): The validation errors from Marshmallow.
        form (FlaskForm): The Flask-WTF form instance.

    Returns:
        None
    """
    for field_name, messages in errors.messages.items():
        field = getattr(form, field_name)
        if isinstance(field.errors, list):
            field.errors.extend(messages)
        else:
            field.errors = list(messages)

