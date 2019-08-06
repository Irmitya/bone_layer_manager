import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty

# Utility functions #


def ShowMessageBox(message="", title="Message Box", icon='INFO'):
    # Simple display message utility

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def get_bones(arm, context, selected):
    # Get armature bones according to current context

    if context.mode == 'EDIT_ARMATURE':
        if selected:
            bones = context.selected_bones
        else:
            bones = arm.edit_bones
    elif context.mode == 'OBJECT':
        if selected:
            bones = []
        else:
            bones = arm.bones
    else:
        if selected:
            # Ugly Try/except to catch weight paint context error if armature is not related to mesh.
            try:
                pose_bones = context.selected_pose_bones
                bones = [b.id_data.data.bones[b.name] for b in pose_bones]
            except TypeError:
                return []
        else:
            bones = arm.bones

    return bones


def check_used_layer(arm, layer_idx, context):
    # Check wether the given layer is used

    bones = get_bones(arm, context, False)

    is_use = 0

    for bone in bones:
        if bone.layers[layer_idx]:
            is_use = 1
            break

    return is_use


def check_selected_layer(arm, layer_idx, context):
    # Check wether selected bones are in layer

    bones = get_bones(arm, context, True)

    is_sel = 0

    for bone in bones:
        if bone.layers[layer_idx]:
            is_sel = 1
            break

    return is_sel


def prefs():
    # Pointer for preferences where UI settings are stored

    return bpy.context.preferences.addons[__package__].preferences
