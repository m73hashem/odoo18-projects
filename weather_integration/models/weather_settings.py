from odoo import models, fields, api


class WeatherConfig(models.Model):
    _name = "weather.config"
    _description = "Weather Configuration"

    weather_api_key = fields.Char(string="Weather API Key")
    default_city = fields.Char(string="Default City")

    name = fields.Char(string="Name", compute="_compute_name", store=False)

    # change the display name
    def _compute_name(self):
        for rec in self:
            rec.name = "Weather Settings"


    # -----------------------------
    # Singleton Logic
    # -----------------------------
    @api.model
    def get_singleton(self):
        """Ensure there's always one record only"""
        record = self.search([], limit=1)
        if not record:
            # create record with values from ir.config_parameter
            config = self.env['ir.config_parameter'].sudo()
            record = self.create({
                "weather_api_key": config.get_param("weather_integration.api_key", ""),
                "default_city": config.get_param("weather_integration.default_city", ""),
            })
        return record



    # -----------------------------
    # Save Hook → Sync with ir.config_parameter
    # -----------------------------
    def write(self, vals):
        res = super().write(vals)
        config = self.env['ir.config_parameter'].sudo()
        if "weather_api_key" in vals:
            config.set_param("weather_integration.api_key", self.weather_api_key or "")
        if "default_city" in vals:
            config.set_param("weather_integration.default_city", self.default_city or "")
        return res

    @api.model
    def action_open_weather_config(self):
        """Return action that opens the singleton record"""
        record = self.get_singleton()
        action = self.env.ref("weather_integration.action_weather_config").sudo().read()[0]
        action.update({
            "res_id": record.id,
            "target": "current",
            "view_mode": "form",
        })
        return action

    def action_save_config(self):
        self.ensure_one()
        config = self.env['ir.config_parameter'].sudo()
        if self.weather_api_key:
            config.set_param("weather_integration.api_key", self.weather_api_key)
        if self.default_city:
            config.set_param("weather_integration.default_city", self.default_city)
        return { #display message of success
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": "Weather settings saved successfully!",
                "sticky": False,
                "type": "success",
            },
        }

