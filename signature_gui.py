from flexx import flx
from caph_widgets import MyWidget, TuiImageEditor
import asyncio

class MyApp_JS(MyWidget):
    CSS = '''
    .equal_width{
        flex-basis: 0;
        text-align: center;
    }
    .holiday{
        background: #f4f4f4;
    }
    .other-month{
        font-style: italic;
        color: #999;
    }
    .today{
        font-weight: bold;
    }
    .text-center{
        text-align: center;
    }
    .large-clock{
        font-size: 3em;
    }
    .calendar-month{
        min-width:8em;
        width:8em;
    }
    '''
    ready = flx.BoolProp(False)

    def init(self):
        super().init()
        with flx.VBox():
            TuiImageEditor(flex=1)
        self._init_ready()
        return

    async def _init_focus(self):
        while self.document.hasFocus()==False:
            await self.sleep(50)
        #self.wprompt.set_focus()
        return

    async def _init_ready(self):
        #while not self.month or not self.rows:
        #    await self.sleep(50)
        self._mutate_ready(True)
        return

    #@flx.reaction('wcalendar.header.children*.pointer_click')
    def _on_click(self, *events):
        e = events[-1]
        v = {'+':'+year', '-':'-year', '⭢':'+month',
            '⭠':'-month'}.get(e.source.text, None)
        if v: self.emit_calendar(v)
        return

    @flx.emitter
    def emit_calendar(self, event):
        return dict(value=event)


class MyApp(flx.PyComponent):

    def init(self):
        self.ready = False
        self.js = MyApp_JS()
        asyncio.ensure_future(self._post_init())
        return

    async def _post_init(self):
        while not self.js.ready:
            await asyncio.sleep(50e-3)
        return

    #@flx.reaction('js.emit_calendar')
    def _on_click_calendar(self, *events):
        return

def main():
    title = 'caph PDF manager'
    icon = None
    app = flx.App(MyApp)
    UI = app.launch('app', title=title, icon=icon)
    #UI = app.launch('chrome-browser', title=title, icon=icon)
    flx.run()
    return

main()
