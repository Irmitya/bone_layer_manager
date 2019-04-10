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
        empty_ui = True

        for ac_ob in objects:
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
                            if (uistart is True):
                                uistart = False
                                empty_ui = False

                                split = layout.row(align=False).split()

                                # Display Rig name
                                row = split.row()
                                if (len(objects) > 1):
                                    row.label(text=ac_ob.name, icon='ARMATURE_DATA')

                                # Export button
                                row = split.row(align=True)
                                row.label(text="Write UI to script", translate=False)
                                row.operator("bone_layer_man.write_rig_ui", emboss=True, text="", icon='TEXT')

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
        if empty_ui:
            layout.label(text="No available UI layers in rigs", icon='INFO')
