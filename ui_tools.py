from PySide6.QtWidgets import QLabel


class StatusText:
    _widget: QLabel | None = None

    @classmethod
    def getWidget(cls) -> QLabel:
        if cls._widget is None:
            cls._widget = QLabel()
        return cls._widget

    @classmethod
    def hide(cls):
        if cls._widget is not None:
            cls._widget.hide()

    @classmethod
    def setText(cls, text: str):
        widget = cls.getWidget()
        if widget is not None:
            if widget.parentWidget():
                widget.setText(text)
                widget.show()
