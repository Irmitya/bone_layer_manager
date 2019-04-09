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
        layout = self.layout
        ac_ob = context.active_object
        scn = context.scene
        objects = [ac_ob] + [o for o in context.selected_objects if o != ac_ob]
        for (i_ob, ac_ob) in enumerate(objects):
            if (ac_ob.type != 'ARMATURE'):
                continue
            uistart = True
            rowstart = True
            endrow = False

            # Iterate through layers creating rows for the Rig UI
            x = 1
            while x < 33:
                rowstart = True
                i = 0
                while i < 33:
                    name_id_prop = f"layer_name_{i}"
                    rigui_id_prop = f"rigui_id_{i}"
                    name = ac_ob.data.get(name_id_prop, "*NO NAME*")
                    uselayer = ac_ob.data.get(rigui_id_prop, 0)

                    # Set start of UI row
                    if uselayer == x and endrow is False:
                        if rowstart is True:
                            # Display Rig name
                            if (uistart is True) and (len(objects) > 1):
                                uistart = False
                                if i_ob:  # Don't use separator on the first rig
                                    layout.separator()
                                layout.label(text=ac_ob.name, icon='ARMATURE_DATA')

                            row = layout.row(align=True)
                            rowstart = False

                        while uselayer < (x + 1):
                            if uselayer == (x + 1):
                                continue
                            row.prop(ac_ob.data, 'layers', index=i, toggle=True, text=name)
                            uselayer += 1
                        # Mark end of current row in iteration
                        if i == 32:
                            endrow = True
                    i += 1

                x += 1

            row = layout.row(align=False)
            split = row.split(align=True, factor=0)

            row = split.row(align=True)
            row.alignment = 'LEFT'
            row.label(text="Swap active layers", translate=False)
            row.operator("bone_layer_man.bonelayerswap", emboss=True, text="", icon='NODETREE')

            row = split.row(align=True)
            row.alignment = 'RIGHT'
            row.label(text="Write UI to script", translate=False)
            row.operator("bone_layer_man.write_rig_ui", emboss=True, text="", icon='TEXT')
