from ui.cmd import CMD
from ui.gui import main
import sys
import alexandria.utils as u

params = u.readSettings()
if params["GUI_useage"]:
    params["GUI_useage"] = False
    u.writeSettings(params)
    raise NotImplementedError("Graphical user interface not implemented yet. Defaulting to terminal useage.")
elif "-d" in sys.argv: # Debugging "mode"
    main(params, True)
else:
    cmd = CMD(params)
    cmd.main()