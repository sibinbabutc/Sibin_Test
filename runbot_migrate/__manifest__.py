{
    'name': 'Runbot Migrate',
    'category': 'Website',
    'summary': 'Runbot Migration tests',
    'version': '1.0',
    'description': "Runbot module to test migration scripts",
    'author': 'Odoo SA',
    'depends': ['runbot'],
    'data': [
        'views/build_views.xml',
        'data/runbot_build_config_data.xml',
    ],
}
