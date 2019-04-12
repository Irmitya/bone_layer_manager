import bpy

from .blmfuncs import get_bones, prefs


class BLTGGLE_OT_toggledefs(bpy.types.Operator):
    '''Toggle Deform Bones Isolated View (Try Shift Click)'''
    bl_idname = "bone_layer_man.deformerisolate"
    bl_label = "Toggle Deform Bone Only View"

    @classmethod
    def poll(self, context):
        if context.mode == 'OBJECT':
            return False
        return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def invoke(self, context, event):
        ac_ob = context.active_object
        arm = ac_ob.data
        bones = get_bones(arm, context, False)

        if event.shift:
            if prefs().BLM_ToggleView_pose:
                for bone in bones:
                    if bone.use_deform is True:
                        bone.hide = True
                prefs().BLM_ToggleView_pose = False

            else:
                for bone in bones:
                    if bone.use_deform is True:
                        bone.hide = False
                prefs().BLM_ToggleView_pose = True

            return {'FINISHED'}
        else:
            if prefs().BLM_ToggleView_deform:
                for bone in bones:
                    if bone.use_deform is False:
                        bone.hide = True
                prefs().BLM_ToggleView_deform = False

            else:
                for bone in bones:
                    if bone.use_deform is False:
                        bone.hide = False
                prefs().BLM_ToggleView_deform = True

            return {'FINISHED'}
