{
    "name": "Real Estate",  # The name that will appear in the App list
    "version": "18.0.1.0.1",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
    "ir.model.access.csv",
    "views/estate_property_views.xml",
    "views/estate_property_type_views.xml",
    "views/estate_property_tags_views.xml",
    "views/estate_property_offer_views.xml",
    "views/estate_menus.xml",
    "views/estate_property_tree.xml",
    "views/estate_property_offer_tree.xml",
    "views/estate_property_form.xml",
    "views/estate_property_search.xml",
    "views/estate_res_user_form.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
