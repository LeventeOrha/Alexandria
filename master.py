from pathlib import Path
from alexandria.error_logging import install_exception_logging

install_exception_logging(Path(__file__).resolve().parent / "logs")

from ui.cmd import CMD
from ui.gui import main
import sys
import alexandria.utils as u

params = u.readSettings()
if (params["GUI_useage"]) and ("-d" not in sys.argv):
    params["GUI_useage"] = False
    u.writeSettings(params)
    raise NotImplementedError("Graphical user interface not implemented yet. Defaulting to terminal useage.")
elif "-d" in sys.argv: # Debugging "mode"
    main(params, True)
else:
    cmd = CMD(params)
    cmd.main()