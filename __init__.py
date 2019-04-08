# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    'name': 'Bone Layer Manager',
    'description': 'Add Bone Layer Name functionality and Rig UI Creation Tools',
    'author': 'Alfonso Annarumma, Paolo Acampora, Fin',
    'version': (0, 7, 1),
    'blender': (2, 80, 0),
    'location': 'View3D > Properties  > Bone Layers',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View'
}

import bpy

from . create_layer_id import CREATEID_OT_name
from . create_rigui_id import SETUIID_OT_riguiid
from . lock_layer import LOCKLAYER_OT_lock
from . select_layer import SELECTLAYER_OT_selectlayer
from . merge_layers import BLMERGE_OT_merge
from . make_group import BLGROUP_OT_group
from . toggle_deform_view import BLTGGLE_OT_toggledefs
from . toggle_deform_prop import BLDEF_OT_deformproptoggle
from . swap_layers import BLSWAP_OT_swaplayers
from . write_ui_script import WRITEUI_OT_writeui
from . bone_layers_panel import BLM_PT_Panel
from . rigui_panel import BLM_PT_Rigui
from . customprop_panel import BLM_PT_customproperties

classes = (
            CREATEID_OT_name,
            SETUIID_OT_riguiid,
            LOCKLAYER_OT_lock,
            SELECTLAYER_OT_selectlayer,
            BLMERGE_OT_merge,
            BLGROUP_OT_group,
            BLTGGLE_OT_toggledefs,
            BLDEF_OT_deformproptoggle,
            BLSWAP_OT_swaplayers,
            WRITEUI_OT_writeui,
            BLM_PT_Panel,
            BLM_PT_Rigui,
            BLM_PT_customproperties,
          )

register, unregister = bpy.utils.register_classes_factory(classes)
