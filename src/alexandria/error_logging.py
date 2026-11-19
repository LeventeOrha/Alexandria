"""Logging support for uncaught application exceptions."""

from __future__ import annotations

import inspect
import re
import sys
import threading
import traceback
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import Type

_LOG_LOCK = threading.Lock()
_SENSITIVE_ARGUMENT = re.compile(
    r"password|secret|token|credential|api.?key|access.?key|private.?key|authorization",
    re.IGNORECASE,
)
_DEFAULT_SYS_EXCEPTHOOK = sys.excepthook
_DEFAULT_THREAD_EXCEPTHOOK = threading.excepthook
_DEFAULT_UNRAISABLEHOOK = sys.unraisablehook


def _safe_repr(name: str, value: object) -> str:
    if _SENSITIVE_ARGUMENT.search(name):
        return "<redacted>"
    if name == "self":
        return f"<{type(value).__name__} instance>"

    try:
        rendered = repr(value)
    except Exception as error:
        rendered = f"<repr failed: {type(error).__name__}>"
    if len(rendered) > 1000:
        rendered = rendered[:997] + "..."
    return rendered


def _format_frame_arguments(tb: TracebackType) -> list[str]:
    frame = tb.tb_frame
    code = frame.f_code
    argument_count = code.co_argcount + code.co_kwonlyargcount
    argument_names = list(code.co_varnames[:argument_count])
    next_index = argument_count

    if code.co_flags & inspect.CO_VARARGS:
        argument_names.append(code.co_varnames[next_index])
        next_index += 1
    if code.co_flags & inspect.CO_VARKEYWORDS:
        argument_names.append(code.co_varnames[next_index])

    lines = []
    for name in argument_names:
        if name in frame.f_locals:
            lines.append(f"    {name} = {_safe_repr(name, frame.f_locals[name])}\n")
    return lines


def _write_exception_log(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
    log_directory: Path,
    context: str | None = None,
) -> None:
    try:
        log_directory.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = log_directory / f"{timestamp}.log"
        with _LOG_LOCK, log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(f"Uncaught exception at {datetime.now().isoformat()}\n")
            if context:
                log_file.write(f"Context: {context}\n")
            log_file.write(f"Exception: {exc_type.__name__}: {exc_value}\n\n")
            log_file.write("Traceback:\n")
            log_file.writelines(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )

            if exc_traceback is not None:
                log_file.write("\nFunction arguments (outermost to innermost):\n")
                current = exc_traceback
                while current is not None:
                    frame = current.tb_frame
                    log_file.write(
                        f"  {frame.f_code.co_filename}:{current.tb_lineno} "
                        f"in {frame.f_code.co_name}\n"
                    )
                    log_file.writelines(_format_frame_arguments(current))
                    current = current.tb_next
                log_file.write("\n")
    except Exception as logging_error:
        print(
            f"Failed to write uncaught exception log: {logging_error}",
            file=sys.stderr,
        )


def install_exception_logging(log_directory: Path) -> None:
    """Write uncaught exceptions and their traceback-frame arguments to disk."""

    log_directory = Path(log_directory)

    def handle_exception(
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        _write_exception_log(exc_type, exc_value, exc_traceback, log_directory)
        _DEFAULT_SYS_EXCEPTHOOK(exc_type, exc_value, exc_traceback)

    def handle_thread_exception(args: threading.ExceptHookArgs) -> None:
        context = f"thread {args.thread.name!r}" if args.thread else "thread"
        _write_exception_log(
            args.exc_type,
            args.exc_value,
            args.exc_traceback,
            log_directory,
            context,
        )
        _DEFAULT_THREAD_EXCEPTHOOK(args)

    def handle_unraisable_exception(args: sys.UnraisableHookArgs) -> None:
        _write_exception_log(
            args.exc_type,
            args.exc_value,
            args.exc_traceback,
            log_directory,
            args.err_msg or "unraisable exception",
        )
        _DEFAULT_UNRAISABLEHOOK(args)

    sys.excepthook = handle_exception
    threading.excepthook = handle_thread_exception
    sys.unraisablehook = handle_unraisable_exception
