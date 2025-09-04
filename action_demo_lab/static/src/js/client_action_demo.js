/* @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class MyClientAction extends Component {
    static template = "action_demo_lab.mytemp123";
}

// تسجيل الـ Client Action في الريجيستري
registry.category("actions").add("event_dashboard.dashboard", MyClientAction);
