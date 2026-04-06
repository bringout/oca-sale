# Copyright 2026 bring.out
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GenerateSubscriptionsWizard(models.TransientModel):
    _name = "generate.subscriptions.wizard"
    _description = "Generate subscriptions wizard"

    invoice_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )
    payment_term_id = fields.Many2one(
        comodel_name="account.payment.term",
        string="Payment Terms",
        help="If set, overrides the partner default payment terms on generated invoices.",
    )
    subscription_ids = fields.Many2many(
        comodel_name="sale.subscription",
        string="Subscriptions",
        default=lambda self: [(6, 0, self.env.context.get("active_ids", []))],
        readonly=True,
    )

    def action_generate(self):
        self.ensure_one()
        subscriptions = self.subscription_ids
        if not subscriptions:
            subscriptions = self.env["sale.subscription"].browse(
                self.env.context.get("active_ids", [])
            )
        return subscriptions.action_generate_subscriptions(
            invoice_date=self.invoice_date,
            payment_term_id=self.payment_term_id,
        )
