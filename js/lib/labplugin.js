import { IpyscoreModel, IpyscoreView, version } from "./index";
import { IJupyterWidgetRegistry } from "@jupyter-widgets/base";

export const helloWidgetPlugin = {
  id: "isedit:plugin",
  requires: [IJupyterWidgetRegistry],
  activate: function (app, widgets) {
    widgets.registerWidget({
      name: "isedit",
      version: version,
      exports: { IpyscoreModel, IpyscoreView },
    });
  },
  autoStart: true,
};

export default helloWidgetPlugin;
