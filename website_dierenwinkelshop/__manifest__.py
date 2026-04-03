# -*- coding: utf-8 -*-
{
    'name': 'Dierenwinkelshop.be Theme',
    'description': 'Website theme for dierenwinkelshop.be',
    'category': 'Theme/eCommerce',
    'version': '19.0.1.0.0',
    'author': 'wedoobe',
    'license': 'LGPL-3',
    'depends': [
        'website_sale',
        'website_sale_wishlist',
        'website_mass_mailing',
    ],
    'data': [
        # Config
        'data/presets.xml',
        'data/website.xml',
        # Pages
        'data/pages/home.xml',
        # Views
        'views/website_templates.xml',
        'views/website_sale_templates.xml',
        'views/snippets/options.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_dierenwinkelshop/static/src/scss/primary_variables.scss',
            'website_dierenwinkelshop/static/src/scss/bootstrap_overridden.scss',
            'website_dierenwinkelshop/static/src/scss/theme.scss',
            'website_dierenwinkelshop/static/src/scss/layout/header.scss',
            'website_dierenwinkelshop/static/src/scss/pages/shop.scss',
            'website_dierenwinkelshop/static/src/scss/pages/product_page.scss',
        ],
    },
}
