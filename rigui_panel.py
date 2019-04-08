import bpy

from .blmfuncs import store_props

class BLM_PT_Rigui(bpy.types.Panel):
    """Creates a Rig UI Panel for based on the assigned Rig_ui_ID """
    bl_category = "Bone Layers"
    bl_label = "Rig UI"
    bl_idname = "BLM_PT_Rigui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    store_props()

    @classmethod
    def poll(self, context):
        if context.object and context.object.type == 'ARMATURE':
            return context.object.data

    def draw(self, context):
        ac_ob = context.active_object
        scn = context.scene
        layout = self.layout
        rowstart = True
        endrow = False

        # Iterate through layers creating rows for the Rig UI
        x = 1
        while x < 33:
            rowstart = True
            i = 0
            while i < 33:
                name_id_prop = "layer_name_%s" % i
                rigui_id_prop = "rigui_id_%s" % i
                name = ac_ob.data.get(name_id_prop , "*NO NAME*")
                uselayer = ac_ob.data.get(rigui_id_prop , 0)

                #Set start of UI row
                if uselayer == x and endrow == False:
                    if rowstart == True:
                        row = layout.row(align=True)
                        rowstart = False

                    while uselayer  < x + 1:
                        if  uselayer == x + 1:
                            continue
                        row.prop(ac_ob.data, 'layers', index=i , toggle=True, text= name)
                        uselayer += 1
                    # Mark end of current row in iteration
                    if i == 32:
                        endrow = True
                i += 1

            x += 1

        row = layout.row(align = False)
        split = row.split(align=True, factor=0)

        row = split.row(align=True)
        row.alignment='LEFT'
        row.label(text="Swap active layers", translate=False)
        row = row.operator("bone_layer_man.bonelayerswap",emboss=True, text="", icon='NODETREE')

        row = split.row(align=True)
        row.alignment='RIGHT'
        row.label(text="Write UI to script", translate=False)
        row = row.operator("bone_layer_man.write_rig_ui",emboss=True, text="", icon='TEXT')
