from . customprop_panel import (BLM_PT_customproperties, BLM_PT_customproperties_options,
                                BLM_PT_customproperties_layout)

from . rigui_panel import BLM_PT_rigui
from . bone_layers_panel import (BLM_PT_panel, BLM_PT_panel_options, BLM_PT_panel_layers)
from . write_ui_script import WRITEUI_OT_writeui
from . swap_layers import BLSWAP_OT_swaplayers
from . toggle_deform_prop import BLDEF_OT_deformproptoggle
from . toggle_deform_view import BLTGGLE_OT_toggledefs
from . make_group import BLGROUP_OT_group
from . merge_layers import BLMERGE_OT_merge
from . select_layer import SELECTLAYER_OT_selectlayer
from . lock_layer import LOCKLAYER_OT_lock
from . create_rigui_id import (SETUIID_OT_riguiid, SETUIID_OT_riguiid2, SETUIID_OT_riguiid3)
from . create_layer_id import CREATEID_OT_name
from . layer_audit import BLM_OT_layeraudit
from . qconstraints_panel import (QC_MT_specials, QC_OT_popup, QC_UL_conlist,
                                  QC_PT_qcontraints, QC_PT_subqcontraints,
                                  QC_PT_ConSettings)

from . constraint_operators import (QC_OT_contraint_action, QC_OT_constraint_add,
                                    QC_OT_remove_target, QC_OT_disable_keep_transform,
                                    QC_OT_copyconstraint, QC_OT_copyall)

from os.path import basename, dirname
from bpy.props import BoolProperty, EnumProperty, IntProperty, FloatProperty

import bpy

bl_info = {
    'name': 'Bone Layer Manager',
    'description': 'Add Bone Layer Name functionality and Rig UI Creation Tools',
    'author': 'Alfonso Annarumma, Paolo Acampora, Fin, COnLOAR',
    'version': (0, 7, 7),
    'blender': (2, 80, 0),
    'location': 'View3D > Properties  > Bone Layers',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View'
}


class BLMpreferences(bpy.types.AddonPreferences):
    bl_idname = __name__  # basename(dirname(__file__))

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        col = row.column()
        col.label(text="Layer Management Defaults:")
        col.prop(self, "BLM_LayerVisibility", text="Hide Empty Layers")
        col.prop(self, "BLM_ExtraOptions", text="Show Extended Layer Options")
        col.prop(self, "BLM_LayerIndex", text="Show Layer Index")
        col.prop(self, "BLM_ShowNamed", text="Show Named Layers Only")
        col.prop(self, "BLM_ShowRigUI", text="Show Rig UI Setup")
        col.prop(self, "BLM_ShowLayerSort", text="Enable Layer Sorting")
        col.prop(self, "BLM_GroupBy", text="Group Layers by")

        col = row.column()
        col.label(text="Custom Properties Defaults:")
        col.prop(self, "BLM_ShowPropEdit", text="Custom Properties Edit")
        col.prop(self, "BLM_ShowBoneLabels", text="Show Bone Labels")
        col.prop(self, "BLM_ShowArmatureName", text="Show Armature Name")
        col.label(text="Slider Size:")
        col.prop(self, "BLM_CustomPropSplit", text="Set Custom Properties Split")

        col = row.column()
        col.label(text="RigUI Options:")
        col.prop(self, "BLM_AddRUIMode", expand=True)

    BLM_AddRUIMode: EnumProperty(
        items=[
            ('default', "Default", "Click to assign layer as ID number"),
            ('new', "New", "Click to assign incremental numbers as ID"),
            ('mix', "Mix", "Click to assign layer as ID number\nCtrl / Shift Click to assign in Increments"),
            ],
        # name="",
        description="Default mode for assiging Rig UI ID",
        # default=None,  # ('string' or {'set'})  from items
        )

    BLM_ActiveRUILayer: IntProperty(
        name="Active Rig UI Layer",
        description="Current UI Layer to add button to",
        min=1,
        max=32,
        default=1)

    BLM_ExtraOptions: BoolProperty(
        name="Show Options",
        description="Show extra options",
        default=True)

    BLM_GroupBy: IntProperty(
        name="Group By",
        description="How many layers per group",
        min=1,
        max=32,
        default=8)

    BLM_LayerVisibility: BoolProperty(
        name="Hide Empty",
        description="Hide empty layers",
        default=False)

    BLM_LayerIndex: BoolProperty(
        name="Show Index",
        description="Show layer Index",
        default=False)

    BLM_ShowArmatureName: BoolProperty(
        name="Show Armature Name",
        description="Show Armature Name",
        default=False)

    BLM_ShowBoneLabels: BoolProperty(
        name="Show Bone Labels",
        description="Show Bone Labels",
        default=False)

    BLM_ShowLayerSort: BoolProperty(
        name="Enable Layer Sorting",
        description="Show Layer Sorting Buttons",
        default=False)

    BLM_ShowNamed: BoolProperty(
        name="Show Named",
        description="Show named layers only",
        default=False)

    BLM_ShowPropEdit: BoolProperty(
        name="Properties Edit",
        description="Edit Bone Properties",
        default=False)

    BLM_ShowRigUI: BoolProperty(
        name="RigUI Setup",
        description="Show Rig UI Setup",
        default=False)

    BLM_ShowSwap: BoolProperty(
        name="Enable UI Layer Swapping",
        description="Enable UI Swapping",
        default=False)

    BLM_ToggleView_deform: BoolProperty(
        name="Toggle Status",
        description="Isolate Deformers",
        default=False)

    BLM_ToggleView_pose: BoolProperty(
        name="Toggle Status",
        description="Isolate pose",
        default=False)

    BLM_UseDeform: BoolProperty(
        name="Use Deform",
        description="Enable Bone to deform geometry",
        default=False)

    BLM_CustomPropSplit: FloatProperty(
        name="Custom Property Panel Splt",
        description="Set Custom Properties Name\Slider Ratio",
        min=.2,
        max=.8,
        default=.6,
        subtype="FACTOR")

classes = (
    BLMpreferences,
    CREATEID_OT_name,
    SETUIID_OT_riguiid, SETUIID_OT_riguiid2, SETUIID_OT_riguiid3,
    LOCKLAYER_OT_lock,
    SELECTLAYER_OT_selectlayer,
    BLMERGE_OT_merge,
    BLGROUP_OT_group,
    BLTGGLE_OT_toggledefs,
    BLDEF_OT_deformproptoggle,
    BLSWAP_OT_swaplayers,
    WRITEUI_OT_writeui,
    BLM_PT_panel,
    BLM_PT_panel_options,
    BLM_PT_panel_layers,
    BLM_PT_rigui,
    BLM_PT_customproperties,
    BLM_PT_customproperties_options,
    BLM_PT_customproperties_layout,
    BLM_OT_layeraudit,
    QC_PT_qcontraints,
    QC_PT_subqcontraints,
    QC_PT_ConSettings,
    QC_UL_conlist,
    QC_OT_contraint_action,
    QC_OT_disable_keep_transform,
    QC_OT_remove_target,
    QC_OT_constraint_add,
    QC_OT_popup,
    QC_MT_specials,
    QC_OT_copyconstraint,
    QC_OT_copyall,

)

register, unregister = bpy.utils.register_classes_factory(classes)
