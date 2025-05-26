from __future__ import annotations

import re
from enum import IntEnum
import logging
from typing import Any, cast, Callable
import inspect
from textwrap import dedent

try:
    from textual import on
    from textual.suggester import Suggester
    from textual.binding import Binding
    from textual.app import App, ComposeResult
    from textual.widgets import (
        Footer,
        Header,
        TabbedContent,
        TabPane,
        Button,
        Input,
        Label,
        Select,
        Log,
        TextArea
    )
    from textual.containers import Grid, HorizontalGroup
    from textual.validation import Validator, ValidationResult
    from rapidfuzz import fuzz, process
except ModuleNotFoundError:
    print(
        """
Missing dependencies. The Interactive Terminal app needs the following
dependencies:
- textual
- rapidfuzz

Install the missing dependencies manually, or install GeoComPy with the
'apps' extra:

pip install geocompy[appps]
"""
    )
    exit(3)

from geocompy import open_serial, GeoCom, GsiOnlineDNA, Angle, Coordinate
from geocompy.communication import Connection


class DummyGeoComConnection(Connection):
    class Port:
        def __init__(self, port: str):
            self.port = port

    _RESP = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+):"
        r"(?P<rc>\d+)"
        r"(?:,(?P<params>.*))?$"
    )

    _CMD = re.compile(
        r"^%R1Q,"
        r"(?P<rpc>\d+):"
        r"(?:(?P<params>.*))?$"
    )

    def __init__(self, port: str):
        self._port = self.Port(port)

    def __enter__(self) -> DummyGeoComConnection:
        return self

    def __exit__(self, *args: Any) -> None:
        return

    def close(self) -> None:
        return

    def send(self, message: str) -> None:
        return

    def exchange(self, cmd: str) -> str:
        if not self._CMD.match(cmd):
            return "%R1P,0,0:2"

        if cmd == "%R1Q,5008:":
            return "%R1P,0,0:0,1996,'07','19','10','13','2f'"

        return "%R1P,0,0:0"


# def open_serial(port: str, **kwargs: Any) -> DummyGeoComConnection:
#     return DummyGeoComConnection(port)


def get_app_logger(app: App[None], name: str) -> logging.Logger:
    log = logging.Logger(name, logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s <%(name)s> [%(levelname)s] %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    handler = logging.StreamHandler(app.query_one("#log_com", Log))
    handler.setFormatter(fmt)
    log.addHandler(handler)
    return log


class Protocol(IntEnum):
    GEOCOM = 0
    GSIDNA = 1


class CmdSuggester(Suggester):
    PATH = re.compile(r"^(\w+(?:\.\w+)*)([\.\(]?)")

    def __init__(self, app: GeoComTerminal):
        super().__init__(use_cache=False, case_sensitive=False)
        self.app = app

    def get_last_valid_obj(self, value: str) -> tuple[Any, str, str] | None:
        if value == "":
            return self.app.protocol, "", "."

        mat = self.PATH.match(value)
        if mat is None:
            return None

        obj = self.app.protocol
        parts: list[str] = []
        namespaces = mat.group(1).split(".")
        for i in range(len(namespaces)):
            p = namespaces.pop(0)
            if not hasattr(obj, p):
                namespaces.insert(0, p)
                break

            obj = getattr(obj, p)
            parts.append(p)

        match len(namespaces):
            case 0:
                partial = "." if mat.group(2) == "." else ""
            case 1:
                partial = namespaces[0]
            case _:
                return None

        path = ".".join(parts)
        return obj, path, partial

    def format_signature(
        self,
        obj: Callable[[Any], Any],
        signature: inspect.Signature
    ) -> str:
        text = f"def {obj.__name__}("

        params: list[str] = []
        for param in signature.parameters.values():
            default = ""
            if param.default is not inspect._empty:
                default = f" = {param.default}"
            params.append(
                f"\t{param.name}: {param.annotation}{default}")

        if len(params) > 0:
            text += f"\n{',\n'.join(params)}\n"

        text += f") -> {signature.return_annotation}\n"

        text += dedent(obj.__doc__) if obj.__doc__ is not None else ""

        return text

    async def get_suggestion(self, value: str) -> str | None:
        info = self.app.query_one("#cmd_info", TextArea)
        # log = self.app.query_one("#log_cmd", Log)

        mat = self.PATH.match(value)
        if value != "" and mat is None:
            # log.write_line("No match")
            info.text = ""
            return None

        result = self.get_last_valid_obj(value)
        if result is None:
            # log.write_line("No object")
            info.text = ""
            return None

        obj, path, partial = result
        if partial == "":
            # log.write_line("No partial")
            if value.removeprefix(path).startswith("("):
                try:
                    info.text = self.format_signature(
                        obj, inspect.signature(obj))
                except Exception:
                    info.text = ""
                return None

            info.text = ""
            return None

        suggest: list[str] = []
        if partial == ".":
            suggest = list(
                filter(lambda s: not s.startswith("_"), dir(obj)))
        else:
            suggest = list(
                filter(
                    lambda s: not s.startswith("_")
                    and fuzz.partial_ratio(partial, s) > 70,
                    dir(obj)
                )
            )

        # log.write_line(f"{suggest}, {obj}, {path}, {partial}")
        if len(suggest) == 0:
            info.text = ""
            return None

        suggestions = ", ".join(suggest)
        info.text = suggestions

        separator = "." if path != "" else ""

        suggestion = process.extractOne(
            partial, suggest, scorer=fuzz.partial_ratio)[0]

        return f"{path}{separator}{suggestion}"


class CmdInput(Input):
    BINDINGS = [
        Binding("escape", "clear", "Clear"),
        Binding("enter", "execute", "Execute"),
        Binding("up", "history('up')", "History"),
        Binding("down", "history('down')", "History")
    ]

    history: list[str] = []
    history_index: int | None = None

    PAT = re.compile(r"(\w+(?:\.\w+)*)\((.*)\)")

    def action_history(self, direction: str) -> None:
        if len(self.history) == 0:
            return

        match direction:
            case 'up':
                if self.history_index is None:
                    self.history_index = 0

                self.history_index = max(
                    self.history_index - 1, -len(self.history))
            case 'down':
                if self.history_index is None:
                    return

                self.history_index = min(self.history_index + 1, 0)
            case _:
                return

        self.value = self.history[self.history_index]
        self.cursor_position = len(self.value)

    def action_clear(self) -> None:
        self.history_index = None
        self.app.query_one("#cmd_info", TextArea).text = ""
        self.clear()

    def action_execute(self) -> None:
        if self.parent is None:
            return

        if not self.PAT.match(self.value):
            self.notify("Not a valid command!",
                        severity="error", title="Error")
            self.app.bell()
            return

        if len(self.history) == 0 or self.value != self.history[-1]:
            self.history.append(self.value)

        self.history_index = None
        app = cast(GeoComTerminal, self.app)
        app.action_execute()


class GeoComTerminal(App[None]):
    CSS_PATH = "app.tcss"
    TITLE = "GeoComPy Interactive Terminal"

    protocol: GeoCom | GsiOnlineDNA | None = None

    def compose(self) -> ComposeResult:
        self.action_show_help_panel()

        with TabbedContent(initial="tab_com"):
            with TabPane("Connection", id="tab_com"):
                with Grid(classes="connect"):
                    yield Label("Port")
                    yield Input(
                        placeholder="COM1",
                        valid_empty=False,
                        validators=[
                            ComPort()
                        ],
                        id="edit_com"
                    )
                    yield Label("Protocol")
                    yield Select(
                        [
                            ("GeoCom", Protocol.GEOCOM),
                            ("GSI Online DNA", Protocol.GSIDNA)
                        ],
                        allow_blank=False,
                        id="select_protocol"
                    )
                with HorizontalGroup(id="hg_buttons"):
                    yield Button("Test Connection", id="btn_test_com")
                    yield Button(
                        "Connect",
                        id="btn_connect",
                        variant="primary"
                    )
                    yield Button(
                        "Disconnect",
                        id="btn_disconnect",
                        disabled=True,
                        variant="error"
                    )

            with TabPane("Commands", id="tab_cmd", disabled=True):
                yield Log(id="log_cmd", highlight=True)
                yield TextArea(id="cmd_info", read_only=True)
                yield CmdInput(id="edit_cmd", placeholder="Type commands...",
                               suggester=CmdSuggester(self),
                               select_on_focus=False)

            with TabPane("Logs", id="tab_logs"):
                yield Log(id="log_com", highlight=True)

        yield Header()
        yield Footer()

    def action_execute(self) -> None:
        cmd_input = self.query_one("#edit_cmd", CmdInput)
        cmd = cmd_input.value
        if cmd == "":
            return

        log = self.query_one("#log_cmd", Log)
        log.write_line(f">>> {cmd}")
        try:
            ans = eval(
                f"self.protocol.{cmd}",
                {},
                {
                    "self": self,
                    "Angle": Angle,
                    "Coordinate": Coordinate
                }
            )
            log.write_line(str(ans))
        except Exception as e:
            log.write_line(str(e))

        cmd_input.action_clear()
        self.query_one("#cmd_info", TextArea).text = ""

    def on_unmount(self) -> None:
        if self.protocol is None:
            return

        self.protocol._conn.close()
        self.protocol = None

    @on(Button.Pressed, "#btn_test_com")
    def btn_test_com_pressed(self, event: Button.Pressed) -> None:
        if event.button is None:
            return

        port = self.query_one("#edit_com", Input)
        if not port.is_valid:
            self.notify(
                "Invalid port identifier given!",
                severity="error",
                title="Error"
            )
            self.bell()
            return
        try:
            with open_serial(port.value) as com:
                match self.query_one("#select_protocol", Select).value:
                    case Protocol.GEOCOM:
                        ans = com.exchange(r"%R1Q,0:\r\n")
                        if ans != "%R1P,0,0:0":
                            raise Exception("Invalid response.")
                    case Protocol.GSIDNA:
                        ans = com.exchange(r"a\r\n")
                        if ans != "?":
                            raise Exception("Invalid response.")

        except Exception as e:
            self.notify(
                f"Connection test failed. ({e})",
                severity="error",
                title="Error"
            )
            self.bell()
            return

        self.notify("Connection test successful!", title="Success")
        self.bell()
        return

    @on(Button.Pressed, "#btn_connect")
    def btn_connect_pressed(self, event: Button.Pressed) -> None:
        if event.button is None:
            return
        port = self.query_one("#edit_com", Input)
        if not port.is_valid:
            self.notify(
                "Invalid port identifier given!",
                severity="error",
                title="Error"
            )
            self.app.bell()
            return
        try:
            log = get_app_logger(self, port.value)
            com = open_serial(port.value)
            match self.query_one("#select_protocol", Select).value:
                case Protocol.GEOCOM:
                    self.protocol = GeoCom(com, log)
                    self.sub_title = f"GeoCom ({com._port.port})"
                case Protocol.GSIDNA:
                    self.protocol = GsiOnlineDNA(com, log)
                    self.sub_title = f"GSI Online DNA ({com._port.port})"

            self.query_one("#btn_test_com").disabled = True
            self.query_one("#btn_disconnect").disabled = False
            event.button.disabled = True
            self.query_one("#edit_com", Input).disabled = True
            self.query_one("#select_protocol", Select).disabled = True
            self.query_one("#tab_cmd", TabPane).disabled = False

            self.notify("Connection successful.", title="Success")
            self.bell()

        except Exception as e:
            self.notify(
                f"Could not connect. ({e})",
                severity="error",
                title="Error"
            )
            self.bell()

    @on(Button.Pressed, "#btn_disconnect")
    def btn_disconnect_pressed(self, event: Button.Pressed) -> None:
        if event.button is None:
            return

        if self.protocol is None:
            return

        try:
            self.protocol._conn.close()
            self.protocol = None
            self.query_one("#btn_test_com").disabled = False
            self.query_one("#btn_connect").disabled = False
            event.button.disabled = True
            self.query_one("#edit_com", Input).disabled = False
            self.query_one("#select_protocol", Select).disabled = False
            self.query_one("#tab_cmd", TabPane).disabled = True
            self.sub_title = ""
        except Exception as e:
            self.notify(
                f"Could not disconnect. ({e})",
                severity="error",
                title="Error"
            )
            self.bell()
            return

        self.notify("Disconnected.", title="Success")
        self.bell()


class ComPort(Validator):
    _WINCOM = re.compile(r"COM\d+")
    _LINUXCOM = re.compile(r"/dev/\w+")

    def validate(self, value: str) -> ValidationResult:
        if self._WINCOM.match(value) or self._LINUXCOM.match(value):
            return self.success()

        return self.failure("Not a valid COM port")
