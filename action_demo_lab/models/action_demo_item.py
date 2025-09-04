from odoo import api, fields, models

class ActionDemoItem(models.Model):
    _name = "action.demo.item"
    _description = "Action Demo Item"

    name = fields.Char(required=True, string="Name")
    description = fields.Text(string="Description")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("processed", "Processed"),
        ],
        default="draft",
        string="Status",
        required=True,
    )

    date = fields.Datetime(string="Date")  # لعرضه في calendar view
    value = fields.Integer(string="Value", default=1)


    #Methods:

    def action_process_item(self):
        """Mark the item as processed"""
        for rec in self:
            rec.state = "processed"

    def action_set_to_draft(self):
        """Set the item to draft"""
        for rec in self:
            rec.state = "draft"

