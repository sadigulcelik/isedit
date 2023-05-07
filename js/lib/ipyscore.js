import { DOMWidgetModel, DOMWidgetView } from "@jupyter-widgets/base";
import { Vex } from "vexflow";

// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be serialized.

export class IpyscoreModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: "IpyscoreModel",
      _view_name: "IpyscoreView",
      _model_module: "isedit",
      _view_module: "isedit",
      _model_module_version: "0.1.0",
      _view_module_version: "0.1.0",
      value: [""],
      nkeys: [["cn/4"]],
      durations: [["q"]],
    };
  }
}

const { Factory, EasyScore, System } = Vex.Flow;
const {
  Voice,
  Renderer,
  Stave,
  StaveNote,
  Accidental,
  Beam,
  Formatter,
  Dot,
  addModifier,
} = Vex.Flow;
export class IpyscoreView extends DOMWidgetView {
  render() {
    this.value_changed();

    // Observe and act on future changes to the value attribute
    this.model.on("change:value", this.value_changed, this);
    this.model.on("change:nkeys", this.value_changed, this);
    this.model.on("change:durations", this.value_changed, this);
  }

  value_changed() {
    this.el.textContent = "";
    this.score_container = document.createElement("div");
    this.score_container.textContent = "";

    const renderer = new Renderer(this.score_container, Renderer.Backends.SVG);

    var all_voices = this.model.get("nkeys");
    var all_durs = this.model.get("durations");
    const context = renderer.getContext();

    renderer.resize(500, 200 * Math.max(all_voices.length, all_durs.length));

    for (
      var voice_num = 0;
      voice_num < Math.max(all_voices.length, all_durs.length);
      voice_num++
    ) {
      console.log(voice_num);
    }

    for (
      var voice_num = 0;
      voice_num < Math.max(all_voices.length, all_durs.length);
      voice_num++
    ) {
      console.log(voice_num);
      var voices = all_voices[voice_num];
      var durs = all_durs[voice_num];
      // console.log(voices);

      context.setFont("Arial", 10);

      // Create a stave of width 400 at position 10, 40.
      const stave = new Stave(10, 20 + 200 * voice_num, 400);

      // Add a clef and time signature.
      stave.addClef("treble").addTimeSignature("4/4");

      // Connect it to the rendering context and draw!
      stave.setContext(context).draw();

      // Create the notes

      function getStaveNote(voice, dur) {
        var note = new StaveNote({ keys: [voice], duration: [dur] });

        if (voice.includes("##")) {
          note = note.addModifier(new Accidental("##"));
        } else if (voice.includes("#")) {
          note = note.addModifier(new Accidental("#"));
        } else if (voice.includes("@")) {
          note = note.addModifier(new Accidental("@"));
        } else if (voice.includes("@@")) {
          note = note.addModifier(new Accidental("@@"));
        }

        if (dur.includes("d")) {
          Dot.buildAndAttach([note]);
        }

        return note;
      }

      var notes = [];
      for (var i = 0; i < Math.max(voices.length, durs.length); i++) {
        notes.push(getStaveNote(voices[i], durs[i]));
      }

      Formatter.FormatAndDraw(context, stave, notes);
    }
    this.map_child = this.el.appendChild(this.score_container);
  }
}
