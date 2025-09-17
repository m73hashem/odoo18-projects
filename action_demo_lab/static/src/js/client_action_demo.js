/* @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class MyClientAction extends Component {
    static template = "action_demo_lab.mytemp123";
}

// dd the Client Action in registry
registry.category("actions").add("event_dashboard.dashboard", MyClientAction);
