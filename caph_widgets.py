from flexx import flx
import os

HERE = os.path.dirname(__file__)

def tui_imports():
    tui_sources = {
        'fabric.js': {
            'cdn': 'https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.0.0-beta.12/fabric.js',
            'local': ('assets_js', 'fabric.js'),
        },
        'tui-color-picker.js': {
            'cdn': 'https://uicdn.toast.com/tui-color-picker/latest/tui-color-picker.js',
            'local': ('assets_js', 'tui-color-picker.js'),
        },
        'tui-code-snippet.js': {
            'cdn': 'https://uicdn.toast.com/tui.code-snippet/latest/tui-code-snippet.js',
            'local': ('assets_js', 'tui-code-snippet.js'),
        },
        'tui-image-editor.css': {
            'cdn': 'https://uicdn.toast.com/tui-image-editor/latest/tui-image-editor.css',
            'local': ('assets_js', 'tui-image-editor.css'),
        },
        'tui-image-editor.js': {
            'cdn': 'https://uicdn.toast.com/tui-image-editor/latest/tui-image-editor.js',
            'local': ('assets_js', 'tui-image-editor.js'),
        },
    }
    for key, value in tui_sources.items():
        if 'local' in value:
            path = os.path.join(HERE, *value['local'])
            with open(path) as f:
                content = f.read()
            flx.assets.associate_asset(__name__, key, content)
        else:
            url = value['cdn']
            print('Pulling cdn: ', url)
            flx.assets.associate_asset(__name__, url)
    return

tui_imports()

class MyWidget(flx.Widget):

    def init(self):
        global eval
        super().init()
        self.sleep = eval("(t)=>new Promise(r=>setTimeout(r, t))")
        self.document = eval("document")
        self.newDate = eval("(...args)=>new Date(...args)")
        self.JSON = eval("JSON")
        self._newCircularReplacer = eval("""() => {
          //https://stackoverflow.com/a/53731154/3671939
          const seen = new WeakSet();
          return (key, value) => {
            if (typeof value === "object" && value !== null) {
              if (seen.has(value)) return;
              seen.add(value);
            }
            return value;
          };
        };""")

    def new(self, obj, *args):
        global window
        return window.Reflect.construct(obj, args)

    def repr(self, obj, indent=None):
        #indent = indent and ' '*indent
        handler = self._newCircularReplacer()
        return self.JSON.stringify(obj, handler, indent)


class TuiImageEditor(MyWidget):
    CSS = """
    .flx-TuiImageEditor {

    }
    """

    def init(self):
        global window
        options = dict(
            includeUI=dict(
                #loadImage=dict(
                #    path='sampleImage.jpg',
                #    name='SampleImage'
                #),
                #theme=blackTheme, # or whiteTheme
                initMenu='filter',
                menuBarPosition='bottom'
            ),
            selectionStyle=dict(
                cornerSize=20,
                rotatingPointOffset=70,
            )
        )
        self.tui = self.new(
            window.tui.ImageEditor,
            self.node, options
        )
        #print(self.node.style)
