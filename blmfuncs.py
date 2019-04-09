import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty

# Utility functions #


def ShowMessageBox(message="", title="Message Box", icon='INFO'):
    """
    Simple display message utility
    """

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def get_bones(arm, context, selected):
    """
    Get armature bones according to current context
    """
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
            pose_bones = context.selected_pose_bones
            bones = [b.id_data.data.bones[b.name] for b in pose_bones]
        else:
            bones = arm.bones

    return bones


def check_used_layer(arm, layer_idx, context):
    """
    Check wether the given layer is used
    """
    bones = get_bones(arm, context, False)

    is_use = 0

    for bone in bones:
        if bone.layers[layer_idx]:
            is_use = 1
            break

    return is_use


def check_selected_layer(arm, layer_idx, context):
    """
    Check wether selected bones are in layer
    """
    bones = get_bones(arm, context, True)

    is_sel = 0

    for bone in bones:
        if bone.layers[layer_idx]:
            is_sel = 1
            break

    return is_sel


def store_props():
    """
    Store properties in the scene for UI settings
    """
    scn_type = bpy.types.Scene

    scn_type.BLM_LayerVisibility = BoolProperty(name="Hide Empty",
                                                description="Hide empty layers",
                                                default=False)

    scn_type.BLM_ExtraOptions = BoolProperty(name="Show Options",
                                             description="Show extra options",
                                             default=True)

    scn_type.BLM_LayerIndex = BoolProperty(name="Show Index",
                                           description="Show layer Index",
                                           default=False)

    scn_type.BLM_ShowNamed = BoolProperty(name="Show Named",
                                          description="Show named layers only",
                                          default=False)

    scn_type.BLM_ShowRigUI = BoolProperty(name="RigUI Setup",
                                          description="Show Rig UI Setup",
                                          default=False)

    scn_type.BLM_ShowPropEdit = BoolProperty(name="Properties Edit",
                                             description="Edit Bone Properties",
                                             default=False)

    scn_type.BLM_LayerVisibility = BoolProperty(name="Hide Empty",
                                                description="Hide empty layers",
                                                default=False)

    scn_type.BLM_ToggleView_deform = BoolProperty(name="Toggle Status",
                                                  description="Isolate Deformers",
                                                  default=False)

    scn_type.BLM_ToggleView_pose = BoolProperty(name="Toggle Status",
                                                description="Isolate pose",
                                                default=False)

    scn_type.BLM_UseDeform = BoolProperty(name="Use Deform",
                                          description="Enable Bone to deform geometry",
                                          default=False)

    scn_type.BLM_GroupBy = IntProperty(name="Group By",
                                       description="How many layers per group",
                                       min=1,
                                       max=32,
                                       default=8)

    scn_type.BLM_ActiveRUILayer = IntProperty(name="Active Rig UI Layer",
                                              description="Current UI Layer to add button to",
                                              min=1,
                                              max=32,
                                              default=1)
