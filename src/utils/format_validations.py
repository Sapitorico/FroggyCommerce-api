import re


def validate_provided(data):
    if not data:
        return 'No data provided'
    return None


def validate_required_field(value):
    if value is None:
        return 'field required'
    return None


def validate_empty_string(value):
    if not isinstance(value, str) or len(value) == 0:
        return 'field must be a non-empty string'
    return None


def validate_number(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return 'field must be a number'
    return None


def validate_min(value, min_length=None):
    if isinstance(value, (int, float)):
        if min_length is not None and value < min_length:
            return f'value must be at least {min_length}'
    elif isinstance(value, str):
        if min_length is not None and len(value) < min_length:
            return f'minimum length is {min_length}'
    elif isinstance(value, list):
        if min_length is not None and len(value) < min_length:
            return f'minimum length is {min_length}'
    return None


def validate_max(value, max_length=None):
    if isinstance(value, (int, float)):
        if max_length is not None and value > max_length:
            return f'value must be at most {max_length}'
    elif isinstance(value, str):
        if max_length is not None and len(value) > max_length:
            return f'maximum length is {max_length}'
    elif isinstance(value, list):
        if max_length is not None and len(value) > max_length:
            return f'maximum length is {max_length}'
    return None


def validate_is_digit(value):
    if not value.isdigit():
        return 'invalid number format'
    return None


def validate_min_words(value, min_words=None):
    if min_words is not None and len(value.split(' ')) < min_words:
        return f'value must have at least {min_words} words'
    return None


def validate_max_words(value, max_words=None):
    if max_words is not None and len(value.split(' ')) > max_words:
        return f'value must have at most {max_words} words'
    return None


def validate_email_format(value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        return 'value is not a valid email address'
    return None


def validate_digit_format(value):
    if not value.isdigit():
        return 'value is not a valid digit'
    return None


def validate_array(value):
    if not isinstance(value, list):
        return 'field must be a list'

    if not value:
        return 'field must not be empty'

    if not all(isinstance(item, dict) for item in value):
        return 'all elements in the list must be dictionaries'

    return None


def validate_boolean(value):
    if not isinstance(value, bool):
        return 'field must be a boolean'
    return None


def validate_value_required(items, subfield, value_required, max_required):
    count = sum(1 for item in items if item.get(subfield) == value_required)
    if count == 0:
        return f'At least one item must have \'{subfield}\' set to \'{value_required}\''
    if max_required is not None and count > max_required:
        return f'No more than {max_required} items can have \'{subfield}\' set to \'{value_required}\''

    return None


def validate(data, schema):
    """
    Validates the given data against the provided schema.

    Args:
        data (dict): The data to be validated.
        schema (dict): The schema containing validation rules.

    Returns:
        str or None: If validation fails, returns an error message indicating the validation failure.
                     If validation succeeds, returns None.
    """
    error = validate_provided(data)
    if error:
        return error

    for field, rules in schema.items():
        value = data.get(field)
        if rules.get('required'):
            error = validate_required_field(value)
            if error:
                return f'\'{field}\': {error}'

        type = rules.get('type')
        if type == 'number':
            error = validate_number(value)
            if error:
                return f'\'{field}\': {error}'

            minimum = rules.get('minimum')
            if minimum is not None:
                error = validate_min(value, minimum)
                if error:
                    return f'\'{field}\': {error}'

            maximum = rules.get('maximum')
            if maximum is not None:
                error = validate_max(value, maximum)
                if error:
                    return f'\'{field}\': {error}'

        elif type == 'string':
            error = validate_empty_string(value)
            if error:
                return f'\'{field}\': {error}'

            minimum = rules.get('minLength')
            if minimum is not None:
                error = validate_min(value, minimum)
                if error:
                    return f'\'{field}\': {error}'

            maximum = rules.get('maxLength')
            if maximum is not None:
                error = validate_max(value, maximum)
                if error:
                    return f'\'{field}\': {error}'

            minimum = rules.get('minWords')
            if minimum is not None:
                error = validate_min_words(value, minimum)
                if error:
                    return f'\'{field}\': {error}'

            maximum = rules.get('maxWords')
            if maximum is not None:
                error = validate_max_words(value, maximum)
                if error:
                    return f'\'{field}\': {error}'

            format = rules.get('format')
            if format == 'email':
                error = validate_email_format(value)
                if error:
                    return f'\'{field}\': {error}'
            if format == 'digit':
                error = validate_digit_format(value)
                if error:
                    return f'\'{field}\': {error}'

        elif type == 'boolean':
            error = validate_boolean(value)
            if error:
                return f'\'{field}\': {error}'

        elif type == 'array':
            error = validate_array(value)
            if error:
                return f"'{field}': {error}"

            minimum = rules.get('minLength')
            if minimum is not None:
                error = validate_min(value, minimum)
                if error:
                    return f'\'{field}\': {error}'

            maximum = rules.get('maxLength')
            if maximum is not None:
                error = validate_max(value, maximum)
                if error:
                    return f'\'{field}\': {error}'

            item_schema = rules.get('items')
            if item_schema:
                for index, item in enumerate(value):
                    error = validate(item, item_schema)
                    if error:
                        return f"'{field}[{index}]': {error}"

                for subfield, subrules in item_schema.items():
                    value_required = subrules.get('valueRequired')
                    max_required = subrules.get('maxRequired')
                    if value_required is not None or max_required is not None:
                        error = validate_value_required(
                            value, subfield, value_required, max_required)
                        if error:
                            return f"'{field}': {error}"
    return None
