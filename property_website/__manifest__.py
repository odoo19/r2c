# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details
{
    'name': 'Property Management - Odoo Community Compatible (With Portal)',
    'description': '''This module will help you to manage your real estate portfolio with 
        Property valuation, Maintenance, Insurance, Utilities and Rent management with reminders for each KPIs.''',
    'category': 'Website',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'website': 'http://serpentcs.in/product/property-management-system',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'depends': [
        'om_account_asset',
        'property',
        'base_geolocalize',
        'payment_paypal',
        'website'
        ],
    'data': [
        'views/assets_views.xml',
        'views/homepage_template.xml',
        'views/crm_lead.xml',
        'data/website_data.xml',
        'views/property_main_template.xml',
        'views/property_login_view.xml',
        'views/rent_properties_onload.xml',
        'views/selected_property_template.xml',
        'views/sell_property_template.xml',
        'views/my_property_template.xml',
        'views/search_property.xml',
        'views/website_property_filter.xml',
        'views/property_footer_template.xml',
        'security/website_security.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_frontend': [
            '/property_website/static/src/js/property_rpc.js',
            '/property_website/static/lib/jquery.ui/jquery_ui_slider.js',
            '/property_website/static/lib/jquery.ui/jquery-ui.css',
            '/property_website/static/src/scss/main.scss',
            '/property_website/static/src/css/style.css',
            '/property_website/static/src/css/gallery-grid.css',
            '/property_website/static/src/css/card.css',
            '/property_website/static/src/js/google_map_script.js'
        ],
    },
    'images': ['static/description/banner.png'],
    'application': True,
    'installable': True,
    'price': 349,
    'currency': 'EUR',
}
