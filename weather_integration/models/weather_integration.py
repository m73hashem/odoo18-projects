from odoo import models, fields

class WeatherIntegration(models.Model):
    _name = "weather.integration"
    _description = "Weather Integration History"
    _order = 'create_date desc' #display results from recent to older creation

    city = fields.Char("City", required=True)
    temperature = fields.Float("Temperature (°C)")
    description = fields.Char("Description")
    queried_at = fields.Datetime("Queried At", default=fields.Datetime.now)
