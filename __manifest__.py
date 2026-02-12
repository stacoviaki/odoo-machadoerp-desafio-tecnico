{
    'name': 'Controle de Combustível',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Controle de abastecimentos e estoque',
    'depends': ['base', 'maintenance'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/abastecimento_views.xml',
        'views/estoque_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}
