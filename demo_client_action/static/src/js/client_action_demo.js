/* @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class DemoClientAction extends Component {

    static template = "demo_client_action.mytemp";
}



// Register the client action
registry.category("actions").add("demo_client_action", DemoClientAction);
