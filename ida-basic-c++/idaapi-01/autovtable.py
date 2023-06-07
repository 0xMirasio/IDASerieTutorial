import idaapi

from libautovtable.util import *

class Kp_Menu_Context(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    @classmethod
    def get_name(self):
        return self.__name__

    @classmethod
    def get_label(self):
        return self.label

    @classmethod
    def register(self, plugin, label):
        self.plugin = plugin
        self.label = label
        instance = self()
        return idaapi.register_action(idaapi.action_desc_t(
            self.get_name(),  
            instance.get_label(), 
            instance
        ))

    @classmethod
    def unregister(self):
        idaapi.unregister_action(self.get_name())

    @classmethod
    def activate(self, ctx):
        return 1

    @classmethod
    def update(self, ctx):
        if ctx.widget_type == idaapi.BWN_DISASM:
            return idaapi.AST_ENABLE_FOR_WIDGET
        return idaapi.AST_DISABLE_FOR_WIDGET

class Searcher(Kp_Menu_Context):
    def activate(self, ctx):
        self.plugin.search()
        return 1

p_initialized = False
#--------------------------------------------------------------------------
# Plugin
#--------------------------------------------------------------------------
class IDAAutoVtable(idaapi.plugin_t):
    comment = "IDAAutoVtable parse and generate automatically structure based on found vtable entries"
    help = ""
    wanted_name = "IDAAutoVtable"
    flags = idaapi.PLUGIN_KEEP
    wanted_hotkey= "Ctrl+Shift+9"

    def init(self):
        global p_initialized
        try:
            Searcher.register(self, "IDAAutoVtable")
        except:
            pass

        if p_initialized is False:
            p_initialized = True
            idaapi.register_action(idaapi.action_desc_t("IDAAutoVtable","IDAAutoVtable imports",Searcher(),None,None,0))
            idaapi.attach_action_to_menu("Search", "IDAAutoVtable", idaapi.SETMENU_APP)
        return idaapi.PLUGIN_KEEP

    def term(self):
        pass

    def main(self):
        print("IDAAutoVtable v0.1 | Thibault Poncetta")

        data_s, data_e = get_segrange_byname(".data.rel.ro")
        vtable_list = find_vtable(data_s, data_e)
        populate_db(vtable_list)
          
    def run(self, arg):
        self.main()


def PLUGIN_ENTRY():
    return IDAAutoVtable()