import requests
from odoo import models, fields
from odoo.exceptions import UserError


class WeatherWizard(models.TransientModel):
    _name = "weather.wizard"
    _description = "Weather Lookup Wizard"

    city = fields.Char("City", required=True)
    temperature = fields.Float("Temperature (°C)", readonly=True)
    description = fields.Char("Description", readonly=True)

    #get weather data from OpenWeather API
    def action_get_weather(self):
        config = self.env['ir.config_parameter'].sudo()
        api_key = config.get_param("weather_integration.api_key")
        default_city = config.get_param("weather_integration.default_city")

        if not api_key:
            raise UserError("Please configure the Weather API Key in Weather Settings.")

        for record in self:
            city = record.city or default_city
            if not city:
                raise UserError("Please enter a city or configure a Default City in Weather Settings.")

            base_url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric",
            }

            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                raise UserError(f"API Error: {response.text}")

            data = response.json()
            record.temperature = data["main"]["temp"]
            record.description = data["weather"][0]["description"]

        # reopen the wizard to show the result
        return {
            "type": "ir.actions.act_window",
            "res_model": "weather.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def action_save_weather(self):
        """يحفظ بيانات الطقس في سجل history"""
        if not self.city or not self.temperature:
            raise UserError("No weather data to save. Please fetch weather first.")

        self.env["weather.integration"].create({
            "city": self.city,
            "temperature": self.temperature,
            "description": self.description,
        })

        return {
            "type": "ir.actions.act_window",
            "name": "Weather History",
            "res_model": "weather.integration",
            "view_mode": "list,form",
            "views": [
                (self.env.ref("weather_integration.view_weather_integration_list").id, "list"),
                (self.env.ref("weather_integration.view_weather_integration_form").id, "form"),
            ],
            "target": "current",
            "flags": {"display_notification": {
                "title": "Success",
                "message": "Result saved successfully",
                "type": "success",
                "sticky": False,
            }},
        }
