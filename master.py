from ui.cmd import CMD
import alexandria.utils as u

params = u.readSettings()
if params["GUI_useage"]:
    params["GUI_useage"] = False
    u.writeSettings(params)
    raise NotImplementedError("Graphical user interface not implemented yet. Defaulting to terminal useage.")
cmd = CMD(params)
cmd.main()