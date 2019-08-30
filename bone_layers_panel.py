import bpy

from .blmfuncs import prefs, check_used_layer, check_selected_layer


class BLM_PT_panel(bpy.types.Panel):  # Created to control layout inside the panel
    # Creates a Panel in the scene context of the properties editor
    bl_category = "Bone Layers"
    bl_label = "Layer Management"
    bl_idname = "BLM_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        for ob in context.selected_objects:  # Check for armature in all objects (Add support for Weight Painting)
            if ob.type == 'ARMATURE':
                return True
            else:
                continue
            return False
            # return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def draw(self, context):
        layout = self.layout


class BLM_PT_panel_options(bpy.types.Panel):
    bl_idname = "BLM_PT_panel_options"
    bl_label = "Display Options"
    bl_parent_id = "BLM_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        for ob in context.selected_objects:  # Check for armature in all objects (Add support for Weight Painting)
            if ob.type == 'ARMATURE':
                return True
            else:
                continue
            return False
            # return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(prefs(), "BLM_ExtraOptions", text="Show Options")
        row.prop(prefs(), "BLM_LayerVisibility", text="Hide Empty")

        row = layout.row()
        row.prop(prefs(), "BLM_LayerIndex", text="Show Index")
        row.prop(prefs(), "BLM_ShowNamed", text="Hide Nameless")

        row = layout.row()
        row.prop(prefs(), "BLM_ShowRigUI", text="Show RigUI Layers")
        row.prop(prefs(), "BLM_ShowLayerSort", text="Enable Sorting")


class BLM_PT_panel_layers(bpy.types.Panel):  # renamed as now is subpanel of BLM_PT_panel
    # Creates a subpanel in the scene context of the properties editor
    bl_idname = "BLM_PT_panel_layers"
    bl_label = ""
    bl_parent_id = "BLM_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(self, context):
        for ob in context.selected_objects:  # Check for armature in all objects (Add support for Weight Painting)
            if ob.type == 'ARMATURE':
                return True
            else:
                continue
            return False
            # return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        if context.mode == 'POSE' and context.active_pose_bone is not None:
            is_deform = context.active_pose_bone.bone.use_deform

        elif context.mode == 'PAINT_WEIGHT' and context.active_pose_bone is not None:
            is_deform = context.active_pose_bone.bone.use_deform

        else:
            is_deform = getattr(context.active_bone, 'use_deform', None)

        row = layout.row()
        # row.label(text="Tom's Toggles:", translate=False) # Tom's a good guy ;)
        row.label(text="Deformer Toggles", translate=False)

        row = layout.row()

        if is_deform:
            row.operator("bone_layer_man.deformtoggle",
                         emboss=True, text="Toggle Deform(ON)")
        else:
            row.operator("bone_layer_man.deformtoggle",
                         emboss=True, text="Toggle Deform(OFF)")

        row.operator("bone_layer_man.deformerisolate",
                     emboss=True, text="Deform Bones Only")

        row = layout.row()
        row.label(text="Bone Layers", translate=False)

        objects = [o for o in context.selected_objects if (o.type == 'ARMATURE')]

        grid = layout.column()

        for (i_ob, ac_ob) in enumerate(objects):
            arm = ac_ob.data

            grid.context_pointer_set('active_object', ac_ob)
            col = grid.column(align=True)
            if len(objects) > 1:
                if i_ob:  # Don't use separator on the first rig
                    col.separator()
                col.label(text=ac_ob.name, icon='ARMATURE_DATA')

            for i in range(len(arm.layers)):
                # layer id property
                name_id_prop = f"layer_name_{i}"
                rigui_id_prop = f"rigui_id_{i}"

                # conditionals needed for interface drawing
                # layer is used
                is_use = check_used_layer(arm, i, context)

                # layer is named RigUIid given
                layer_name = None
                rigui_id = None

                try:
                    layer_name = arm[name_id_prop]
                except KeyError:
                    do_name_operator = "bone_layer_man.layout_do_name"
                try:
                    rigui_id = arm[rigui_id_prop]
                except KeyError:
                    do_id_operator = "bone_layer_man.rigui_set_id"

                # Add layer line
                if ((is_use or not prefs().BLM_LayerVisibility) and
                        (layer_name or not prefs().BLM_ShowNamed)):
                    # Group every GroupBy layers
                    if i % prefs().BLM_GroupBy == 0:
                        col.separator()

                    # Fill entries
                    row = col.row(align=True)

                    # visibility, show layer index as text and set split if queried
                    # if visable
                    if prefs().BLM_LayerIndex:
                        split = row.split(align=True, factor=0.2)
                        split.prop(arm, "layers", index=i, emboss=True,
                                   icon=('HIDE_ON', 'HIDE_OFF')[arm.layers[i]],
                                   toggle=True,
                                   text=(f"{i + 1}"))

                        # name if any, else naming operator
                        if layer_name is not None:
                            split.prop(arm, f'["{name_id_prop}"]', text="")
                        else:
                            name_op = split.operator(do_name_operator)
                            name_op.layer_idx = i
                            name_op.layer_name = f"Layer {i + 1}"
                    # else if not visable
                    else:
                        row.prop(arm, "layers", index=i, emboss=True,
                                 icon=('HIDE_ON', 'HIDE_OFF')[arm.layers[i]],
                                 toggle=True,
                                 text="")

                        # name if any, else naming operator
                        if layer_name is not None:
                            row.prop(arm, f'["{name_id_prop}"]', text="")
                        else:
                            name_op = row.operator(do_name_operator)
                            name_op.layer_idx = i
                            name_op.layer_name = f"Layer {i + 1}"

                    # protected layer
                    if prefs().BLM_ExtraOptions:
                        row.prop(arm, "layers_protected", index=i, emboss=True,
                                 icon=('UNLINKED', 'LINKED')[arm.layers_protected[i]],
                                 toggle=True, text="")

                    # RigUI Setup fields

                    if prefs().BLM_ShowRigUI:

                        if rigui_id is None:
                            id_mode = prefs().BLM_AddRUIMode

                            if id_mode == 'new':
                                #  Use sequential number
                                id_op = row.operator("bone_layer_man.rigui_set_id2")
                            else:
                                #  Use layer number
                                if id_mode == 'default':
                                    id_op = row.operator('bone_layer_man.rigui_set_id')
                                if id_mode == 'mix':
                                    id_op = row.operator('bone_layer_man.rigui_set_id3')
                                id_op.rigui_id = i + 1
                            id_op.layer_idx = i
                        else:
                            if rigui_id in range(1, 33):
                                row.prop(arm, f'["{rigui_id_prop}"]', index=i, text="UI Layer ")
                            else:
                                row.prop(arm, f'["{rigui_id_prop}"]', index=i, text="Non UI Layer")

                    # assume layer was never locked if has no lock property
                    lock = arm.get(f"layer_lock_{i}", False)

                    # Select, Lock, Group and Merge are optional
                    if prefs().BLM_ExtraOptions and context.mode != 'OBJECT':
                        # bones select
                        sel_op = row.operator("bone_layer_man.selectboneslayer",
                                              icon='RESTRICT_SELECT_OFF',
                                              text="", emboss=True)
                        sel_op.layer_idx = i

                        if is_use:
                            is_use += check_selected_layer(arm, i, context)
                        merge_op = row.operator("bone_layer_man.blmergeselected",
                                                text="", emboss=True,
                                                icon=('RADIOBUT_OFF',
                                                      'LAYER_USED',
                                                      'LAYER_ACTIVE')[is_use])
                        merge_op.layer_idx = i

                        # groups operator **only in pose mode
                        if context.mode == 'POSE':
                            grp_op = row.operator("bone_layer_man.bonelayergroup",
                                                  text="",
                                                  emboss=True, icon='GROUP_BONE')
                            grp_op.layer_idx = i

                        # lock operator
                        lock_op = row.operator("bone_layer_man.bonelockselected",
                                               text="", emboss=True,
                                               icon=('UNLOCKED', 'LOCKED')[lock])

                        lock_op.layer_idx = i
                        lock_op.lock = not lock

                    def is_lock(idx):
                        # check if layer is locked (or hidden)
                        layer_lock = f"layer_lock_{idx}"
                        lock = arm.get(layer_lock, False)

                        if idx not in range(32):
                            return True
                        at_end = idx in [0, 31]

                        scn = context.scene
                        if not lock and not at_end:
                            is_use = check_used_layer(arm, idx, context)
                            layer_name = arm.get(f"layer_name_{idx}")

                            if not ((is_use or not prefs().BLM_LayerVisibility) and
                                    (layer_name or not prefs().BLM_ShowNamed)):
                                lock = True  # skip hidden layers
                        return lock

                    # Show Sorting functions without "ExtraOptions" enabled
                    if prefs().BLM_ShowLayerSort:

                        # Swap layers button
                        swap = row.row(align=True)
                        swap.enabled = not lock
                        swap.active = True
                        toggle_layer_1 = arm.get('BLM_TEMP_FIRST_LAYER')
                        highlight = bool(toggle_layer_1 == i)

                        if highlight:
                            icon = 'FILE_REFRESH'
                        elif toggle_layer_1:
                            icon = 'LOOP_FORWARDS'
                        else:
                            icon = 'ARROW_LEFTRIGHT'
                        op = swap.operator("bone_layer_man.bonelayerswap", depress=highlight, text="", icon=icon)
                        op.layer_idx = i

                        # Directional layer swapping
                        swap = swap.column(align=True)
                        swap.active = bool(toggle_layer_1 is None)

                        target_up = (i - 1)
                        target_down = (i + 1)

                        while is_lock(target_up) and target_up in range(32):
                            target_up -= 1
                        while is_lock(target_down) and target_down in range(32):
                            target_down += 1

                        if target_up <= 0:
                            icon_up = 'TRIA_UP_BAR'
                        else:
                            icon_up = 'TRIA_UP'

                        if target_down >= 31:
                            icon_down = 'TRIA_DOWN_BAR'
                        else:
                            icon_down = 'TRIA_DOWN'

                        # Diabled sorting method
                        # do_up = not is_lock(target_up)
                        # do_down = not is_lock(target_down)

                        do_up = False
                        do_down = False

                        if (do_up and do_down):
                            swap.scale_y = 0.5

                        if do_up:
                            up = swap.row()
                            op = up.operator("bone_layer_man.bonelayerswap", text="", icon=icon_up)
                            op.layer_idx = i
                            op.target_idx = target_up

                        if do_down:
                            down = swap.row()
                            op = down.operator("bone_layer_man.bonelayerswap", text="", icon=icon_down)
                            op.layer_idx = i
                            op.target_idx = target_down

        row = layout.row()
        row.operator("bone_layer_man.layeraudit",
                     emboss=True, text="Layer Audit")
