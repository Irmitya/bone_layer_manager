import bpy

from .blmfuncs import get_bones


class BLTGGLE_OT_toggledefs(bpy.types.Operator):
    '''Toggle Deform Bones Isolated View (Try Shift Click)'''
    bl_idname = "bone_layer_man.deformerisolate"
    bl_label = "Toggle Deform Bone Only View"

    @classmethod
    def poll(self, context):

        if context.mode == 'OBJECT':
            return False
        try:
            return (context.active_object.type == 'ARMATURE')
        except (AttributeError, KeyError, TypeError):
            return False

    def invoke(self, context, event):
        scn = context.scene
        ac_ob = context.active_object
        arm = ac_ob.data
        bones = get_bones(arm, context, False)

        if event.shift:
            if scn.BLM_ToggleView_pose:
                for bone in bones:
                    if bone.use_deform is True:
                        bone.hide = True
                scn.BLM_ToggleView_pose = False

            else:
                for bone in bones:
                    if bone.use_deform is True:
                        bone.hide = False
                scn.BLM_ToggleView_pose = True

            return {'FINISHED'}
        else:
            if scn.BLM_ToggleView_deform:
                for bone in bones:
                    if bone.use_deform is False:
                        bone.hide = True
                scn.BLM_ToggleView_deform = False

            else:
                for bone in bones:
                    if bone.use_deform is False:
                        bone.hide = False
                scn.BLM_ToggleView_deform = True

            return {'FINISHED'}
