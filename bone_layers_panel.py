import bpy

from .blmfuncs import store_props, check_used_layer, check_selected_layer


class BLM_PT_panel(bpy.types.Panel):  # Created to control layout inside the panel
    """Creates a Panel in the scene context of the properties editor"""
    bl_category = "Bone Layers"
    bl_label = "Layer Management"
    bl_idname = "BLM_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def draw(self, context):
        layout = self.layout


class BLM_PT_panel_options(bpy.types.Panel):
    bl_idname = "BLM_PT_panel_options"
    bl_label = "Display Options"
    bl_parent_id = "BLM_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    store_props()

    @classmethod
    def poll(self, context):
        return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        row = layout.row()
        row.prop(scn, "BLM_ExtraOptions", text="Show Options")
        row.prop(scn, "BLM_LayerVisibility", text="Hide Empty")

        row = layout.row()
        row.prop(scn, "BLM_LayerIndex", text="Show Index")
        row.prop(scn, "BLM_ShowNamed", text="Hide Nameless")

        row = layout.row()
        row.prop(scn, "BLM_ShowRigUI", text="Show RigUI Layers")
        row.prop(scn, "BLM_ShowLayerSort", text="Enable Sorting")


class BLM_PT_panel_layers(bpy.types.Panel):  # renamed as now is subpanel of BLM_PT_panel
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "BLM_PT_panel_layers"
    bl_label = ""
    bl_parent_id = "BLM_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    store_props()

    @classmethod
    def poll(self, context):
        return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        if context.mode == 'POSE' and context.active_pose_bone is not None:
            is_deform = context.active_pose_bone.bone.use_deform
        else:
            is_deform = context.active_bone.use_deform

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

        ac_ob = context.active_object
        objects = [ac_ob] + [o for o in context.selected_objects if o != ac_ob]
        for (i_ob, ac_ob) in enumerate(objects):
            if (ac_ob.type != 'ARMATURE'):
                continue

            layout.context_pointer_set('active_object', ac_ob)
            col = layout.column(align=True)
            if len(objects) > 1:
                if i_ob:  # Don't use separator on the first rig
                    col.separator()
                col.label(text=ac_ob.name, icon='ARMATURE_DATA')

            for i in range(len(ac_ob.data.layers)):
                # layer id property
                name_id_prop = "layer_name_%s" % i
                rigui_id_prop = "rigui_id_%s" % i

                # conditionals needed for interface drawing
                # layer is used
                is_use = check_used_layer(ac_ob.data, i, context)

                # layer is named RigUIid given
                layer_name = None
                rigui_id = None

                try:
                    layer_name = ac_ob.data[name_id_prop]
                except KeyError:
                    do_name_operator = "bone_layer_man.layout_do_name"
                try:
                    rigui_id = ac_ob.data[rigui_id_prop]
                except KeyError:
                    do_id_operator = "bone_layer_man.rigui_set_id"

                # Add layer line
                if ((is_use or not scn.BLM_LayerVisibility) and
                        (layer_name or not scn.BLM_ShowNamed)):
                    # Group every GroupBy layers
                    if i % scn.BLM_GroupBy == 0:
                        col.separator()

                    # Fill entries
                    row = col.row(align=True)

                    # visibility, show layer index as text and set split if queried
                    # if visable
                    if scn.BLM_LayerIndex:
                        split = row.split(align=True, factor=0.2)
                        split.prop(ac_ob.data, "layers", index=i, emboss=True,
                                   icon=('VISIBLE_IPO_OFF', 'VISIBLE_IPO_ON')[ac_ob.data.layers[i]],
                                   toggle=True,
                                   text=(f"{i + 1}"))

                        # name if any, else naming operator
                        if layer_name is not None:
                            split.prop(ac_ob.data, f'["{name_id_prop}"]', text="")
                        else:
                            name_op = split.operator(do_name_operator)
                            name_op.layer_idx = i
                            name_op.layer_name = f"Layer {i + 1}"
                    # else if not visable
                    else:
                        row.prop(ac_ob.data, "layers", index=i, emboss=True,
                                 icon=('VISIBLE_IPO_OFF', 'VISIBLE_IPO_ON')[ac_ob.data.layers[i]],
                                 toggle=True,
                                 text="")

                        # name if any, else naming operator
                        if layer_name is not None:
                            row.prop(ac_ob.data, f'["{name_id_prop}"]', text="")
                        else:
                            name_op = row.operator(do_name_operator)
                            name_op.layer_idx = i
                            name_op.layer_name = f"Layer {i + 1}"

                    # protected layer
                    if scn.BLM_ExtraOptions:
                        row.prop(ac_ob.data, "layers_protected", index=i, emboss=True,
                                 icon=('UNLINKED', 'LINKED')[ac_ob.data.layers_protected[i]],
                                 toggle=True, text="")

                    # RigUI Setup fields
                    if scn.BLM_ShowRigUI:
                        if rigui_id is not None:
                            # row.prop(ac_ob.data, f'["{rigui_id_prop}"]', index=i, text="UI Layer ")
                            if (rigui_id > 0) and (rigui_id < 33):
                                row.prop(
                                    ac_ob.data, f'["{rigui_id_prop}"]', index=i, text="UI Layer ")
                            else:
                                row.prop(
                                    ac_ob.data, f'["{rigui_id_prop}"]', index=i, text="Hidden Layer")
                        else:
                            id_op = row.operator("bone_layer_man.rigui_set_id")
                            id_op.layer_idx = i
                            id_op.rigui_id = i + 1
                            if ac_ob.data.get(rigui_id_prop):
                                row.prop(
                                    ac_ob.data, f'["{rigui_id_prop}"]', index=i, text="")

                    # Select, Lock, Group and Merge are optional
                    if scn.BLM_ExtraOptions and context.mode != 'OBJECT':
                        # bones select
                        sel_op = row.operator("bone_layer_man.selectboneslayer",
                                              icon='RESTRICT_SELECT_OFF',
                                              text="", emboss=True)
                        sel_op.layer_idx = i

                        # col = move_col
                        if is_use:
                            is_use += check_selected_layer(
                                ac_ob.data, i, context)
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
                        lock_id_prop = f"layer_lock_{i}"
                        # assume layer was never locked if has no lock property
                        try:
                            lock = ac_ob.data[lock_id_prop]
                        except KeyError:
                            lock = False

                        lock_op = row.operator("bone_layer_man.bonelockselected",
                                               text="", emboss=True,
                                               icon=('UNLOCKED', 'LOCKED')[lock])

                        lock_op.layer_idx = i
                        lock_op.lock = not lock

                    # Show Sorting functions without "ExtraOptions" enabled
                    if scn.BLM_ShowLayerSort:
                        # lock operator
                        lock_id_prop = f"layer_lock_{i}"
                        # assume layer was never locked if has no lock property
                        try:
                            lock = ac_ob.data[lock_id_prop]
                        except KeyError:
                            lock = False

                        # Swap layers button
                        swap = row.row(align=True)
                        swap.enabled = not lock
                        swap.active = True
                        toggle_layer_1 = ac_ob.data.get('BLM_TEMP_FIRST_LAYER')
                        highlight = bool(toggle_layer_1 == i)

                        if highlight:
                            icon = 'NODE_COMPOSITING'
                        elif toggle_layer_1:
                            icon = 'NODETREE'
                        else:
                            icon = 'NODE'
                        op = swap.operator("bone_layer_man.bonelayerswap", depress=highlight, text="", icon=icon)
                        op.layer_idx = i

                        # Directional layer swapping
                        swap = swap.column(align=True)
                        swap.active = bool(toggle_layer_1 is None)

                        def is_lock(idx):
                            # check if layer is locked (or hidden)
                            arm = ac_ob.data
                            layer_lock = f"layer_lock_{idx}"
                            lock = arm.get(layer_lock, False)

                            if idx not in range(32):
                                return True
                            at_end = idx in [0, 31]

                            scn = context.scene
                            if not lock and not at_end:
                                is_use = check_used_layer(arm, idx, context)
                                layer_name = arm.get(f"layer_name_{idx}")

                                if not ((is_use or not scn.BLM_LayerVisibility) and
                                        (layer_name or not scn.BLM_ShowNamed)):
                                    lock = True  # skip hidden layers
                            return lock

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

                        do_up = not is_lock(target_up)
                        do_down = not is_lock(target_down)

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
