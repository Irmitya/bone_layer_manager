import bpy

from bpy.props import BoolProperty
from .blmfuncs import prefs


class BLM_OT_layeraudit(bpy.types.Operator):
    # Toggle All Selected Bones Deform Property
    bl_idname = "bone_layer_man.layeraudit"
    bl_label = "Clean Layers"
    bl_description = "Reset Empty Layer Names and Non RigUI Layers"

    @classmethod
    def poll(self, context):
        for ob in context.selected_objects:
            if ob.type == 'ARMATURE':
                return True
            else:
                continue
            return False

    def execute(self, context):
        objects = [o for o in context.selected_objects if (o.type == 'ARMATURE')]

        for ac_ob in objects:
            arm = ac_ob.data

            for i in range(len(arm.layers)):
                    # layer id property
                name_id_prop = f"layer_name_{i}"
                rigui_id_prop = f"rigui_id_{i}"
                reset_rigui = arm.get(rigui_id_prop, None)
                reset_layername = arm.get(name_id_prop, None)

                if reset_rigui is not None and reset_rigui == 0:
                    del arm[rigui_id_prop]

                if reset_layername is not None and reset_layername == "":
                    del arm[name_id_prop]

        return {'FINISHED'}
