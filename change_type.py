__author__ = 'Dei'


# 枚举所有能识别的ChangeType


def change_type_enum():
    change_type = ['Additional Class', 'Parent Class Insert',
                   'Decorator Insert',
                   'Additional Functionality',
                   'Statement Insert', 'Method Call Insert',  'Yield Insert',
                   'If Insert',
                   'Else Part Insert',
                   'Loop Insert',
                   'Locational Parameter Insert', 'Variable Parameter Insert', 'Keyword Parameter Insert',
                   'Variable Keyword Parameter Insert', 'Default Locational Parameter Insert',
                   'Default Keyword Parameter Insert',
                   'ReturnValue Insert', 'Return Insert',

                   'Removed Class', 'Parent Class Delete',
                   'Decorator Delete',
                   'Removed Functionality',
                   'Statement Delete', 'Method Call Delete', 'Yield Delete',
                   'If Delete',
                   'Else Part Delete',
                   'Loop Delete',
                   'Locational Parameter Delete', 'Variable Parameter Delete', 'Keyword Parameter Delete',
                   'Variable Keyword Parameter Delete', 'Default Locational Parameter Delete',
                   'Default Keyword Parameter Delete',
                   'ReturnValue Delete', 'Return Delete',

                   'Statement Parent Change',

                   'Function Renaming',
                   'Parameter Renaming',
                   'Conditional Expression Change',
                   'Statement Update', 'Method Call Update', 'Yield Update',
                   'Class Renaming', 'Parent Class Update',
                   'Other Change Type']
    return change_type


