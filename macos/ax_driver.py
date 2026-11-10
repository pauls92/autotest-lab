"""macOS アクセシビリティAPIによる最小限の操作ドライバ。

方針メモ 第4章の「ロケータの優先順位」を実装している:
  1. identifier  2. title / description（ラベル）  3. role + 位置
画像マッチングは持たない。

使い方:
    from ax_driver import App
    app = App("com.apple.TextEdit")
    app.find(identifier="NewDocumentButton").press()
    area = app.wait_for(role="AXTextArea")
    area.set_value("こんにちは")
"""
import os
import time

import AppKit
from ApplicationServices import (
    AXUIElementCopyAttributeValue,
    AXUIElementCreateApplication,
    AXUIElementPerformAction,
    AXUIElementSetAttributeValue,
    kAXChildrenAttribute,
    kAXDescriptionAttribute,
    kAXIdentifierAttribute,
    kAXPressAction,
    kAXRoleAttribute,
    kAXSubroleAttribute,
    kAXTitleAttribute,
    kAXValueAttribute,
)


class NotFound(Exception):
    pass


# デモ用: AX_SLOW=1.5 のように秒数を指定すると、各操作の前にその時間だけ止まる
SLOW = float(os.environ.get("AX_SLOW", "0") or 0)


class Element:
    def __init__(self, ref, path=""):
        self.ref = ref
        self.path = path

    # --- 属性 ---
    def attr(self, name):
        err, val = AXUIElementCopyAttributeValue(self.ref, name, None)
        return val if err == 0 else None

    @property
    def role(self): return self.attr(kAXRoleAttribute)
    @property
    def subrole(self): return self.attr(kAXSubroleAttribute)
    @property
    def title(self): return self.attr(kAXTitleAttribute)
    @property
    def description(self): return self.attr(kAXDescriptionAttribute)
    @property
    def identifier(self): return self.attr(kAXIdentifierAttribute)
    @property
    def value(self): return self.attr(kAXValueAttribute)
    @property
    def children(self):
        return [Element(c, f"{self.path}/{i}") for i, c in enumerate(self.attr(kAXChildrenAttribute) or [])]

    # --- 操作 ---
    def press(self):
        if SLOW:
            print(f"      → press {self}")
            time.sleep(SLOW)
        err = AXUIElementPerformAction(self.ref, kAXPressAction)
        # -25204 (kAXErrorCannotComplete) は、押した結果アプリがモーダルを開いて
        # AX呼び出しがタイムアウトしたときに返る。操作自体は実行済みのことが多いので、
        # ここでは失敗にせず、呼び出し側が wait_for で結果の画面を検証する前提にする。
        if err not in (0, -25204):
            raise RuntimeError(f"AXPress failed ({err}) on {self}")
        return self

    def set_value(self, value):
        if SLOW:
            print(f"      → set {self} = {value!r}")
            time.sleep(SLOW)
        err = AXUIElementSetAttributeValue(self.ref, kAXValueAttribute, value)
        if err != 0:
            raise RuntimeError(f"set value failed ({err}) on {self}")
        return self

    # --- 探索 ---
    def matches(self, identifier=None, title=None, role=None, subrole=None):
        if identifier is not None and self.identifier != identifier:
            return False
        if role is not None and self.role != role:
            return False
        if subrole is not None and self.subrole != subrole:
            return False
        if title is not None and title not in (self.title, self.description):
            return False
        return True

    def walk(self, max_depth=30):
        stack = [(self, 0)]
        while stack:
            el, d = stack.pop()
            yield el
            if d < max_depth:
                stack.extend((c, d + 1) for c in reversed(el.children))

    def find_all(self, **q):
        return [el for el in self.walk() if el.matches(**q)]

    def find(self, **q):
        for el in self.walk():
            if el.matches(**q):
                return el
        raise NotFound(q)

    def wait_for(self, timeout=5.0, interval=0.2, **q):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                return self.find(**q)
            except NotFound:
                time.sleep(interval)
        raise NotFound(f"{q} (timeout {timeout}s)")

    def __repr__(self):
        return f'<{self.role} id={self.identifier!r} title={self.title!r}>'


class App(Element):
    def __init__(self, bundle_id, launch=True, timeout=10.0):
        ws = AppKit.NSWorkspace.sharedWorkspace()
        app = self._running(ws, bundle_id)
        if app is None and launch:
            import subprocess
            subprocess.run(["open", "-b", bundle_id], check=False)
            deadline = time.time() + timeout
            while app is None and time.time() < deadline:
                time.sleep(0.3)
                app = self._running(ws, bundle_id)
        if app is None:
            raise RuntimeError(f"{bundle_id} が起動していません")
        self.ns_app = app
        super().__init__(AXUIElementCreateApplication(app.processIdentifier()), bundle_id)

    @staticmethod
    def _running(ws, bundle_id):
        for a in ws.runningApplications():
            if a.bundleIdentifier() == bundle_id:
                return a
        return None

    def activate(self):
        self.ns_app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
        time.sleep(0.3)
        return self

    def windows(self):
        return [c for c in self.children if c.role == "AXWindow"]
