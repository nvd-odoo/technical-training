{
    "name": "Real Estate account",  # The name that will appear in the App list
    "version": "18.0.1.0.1",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["estate","account"],  # dependencies
    "data": [
        "views/real_estate_form.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}