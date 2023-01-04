import environ


env = environ.Env()
environ.Env.read_env('.env.dev')


def is_procurement_officer():
    return env('PROCUREMENT_OFFICER')


def is_procurement_committee():
    return env('PROCUREMENT_COMMITTEE')


def is_head_finance():
    return env('IS_HEAD_OF_FINANCE')


def is_head_department():
    return env('HEAD_OF_DEPARTMENT')


def is_ceo():
    return env('IS_CEO')


def default():
    return 0


switcher = {
    'is_procurement_officer': is_procurement_officer,
    'is_procurement_committee': is_procurement_committee,
    'is_head_finance': is_head_finance,
    'is_head_department': is_head_department,
    'is_ceo': is_ceo,
}


def get_weight(user):
    return switcher.get(user, default)()
