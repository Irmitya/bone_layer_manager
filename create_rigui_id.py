import bpy

from bpy.props import IntProperty


class SETUIID_OT_riguiid(bpy.types.Operator):
    """Assign and store a layer index for this layer as ID prop"""
    bl_idname = "bone_layer_man.rigui_set_id"
    bl_label = "Assign RigUI Layer"
    bl_description = "Assign a layer index for the RigUI"
    bl_options = {'REGISTER', 'UNDO'}

    layer_idx: IntProperty(name="Layer Index",
                           description="Index of the layer to be named",
                           default=0, min=0, max=31)

    rigui_id: IntProperty(name="RigUI Layer",
                          description="Index of the RigUI layer",
                          default=0, min=0, max=31, soft_min=0, soft_max=31)

    @classmethod
    def poll(self, context):
        arm = getattr(context.active_object, 'data', None)
        not_link = (getattr(arm, 'library', None) is None)
        return not_link

    def execute(self, context):
        arm = bpy.context.active_object.data
        # Create ID prop by setting it
        arm[f"rigui_id_{self.layer_idx}"] = self.rigui_id

        return {'FINISHED'}
