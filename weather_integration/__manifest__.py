{
    "name": "Weather Integration",
    "version": "1.0",
    "category": "Tools",
    "summary": "Integration with OpenWeather API",
    "description": "Fetch and display weather data from OpenWeather API.",
    "author": "Mahmoud Hashem",

    "depends": ["base", 'web'],

    "data": [
        'security/ir.model.access.csv',
        #"data/default_settings.xml",
        'views/weather_settings_view.xml',
        "views/weather_integration_views.xml",
        "views/weather_wizard_views.xml",
    ],

    "installable": True,
    "application": True,
}
