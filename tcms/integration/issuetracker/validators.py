# -*- coding: utf-8 -*-

import importlib
import re
import six

from django.core.exceptions import ValidationError


def validate_class_path(value):
    module_path, _, class_name = value.rpartition('.')
    try:
        module = importlib.import_module(module_path)
    except Exception:
        raise ValidationError('Cannot import {}'.format(module_path))
    if not hasattr(module, class_name):
        raise ValidationError('Module {} does not have class {}'.format(
            module_path, class_name))


def validate_reg_exp(value):
    try:
        re.compile(value)
    except Exception as e:
        raise ValidationError(
            'Regular expression "{}" cannot be compiled by '
            'Python re module. Error: {}'.format(value, str(e)))


def validate_issue_report_params(value):
    """Validate IssueTracker.issue_report_params

    This is a validator assigned to model's validators parameter.
    """
    buf = six.StringIO(value)
    param_lines = buf.readlines()
    buf.close()
    for line in param_lines:
        line = line.rstrip()
        colon_count = line.count(':')
        if colon_count == 0:
            raise ValidationError(
                "Line '{}' is not a pair of key/value separated by ':'.")
        if colon_count > 1:
            raise ValidationError(
                "Line '{}' contains multiple ':'.".format(line))

    # TODO: what other points to check?
