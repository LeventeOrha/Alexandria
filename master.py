from ui.cmd import CMD
import alexandria.utils as u

params = u.readSettings()
cmd = CMD(params)
cmd.main()