bl_info = {
    "name": "Pixelate Addon",
    "author": "hifichevymane",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "Compositor > Toolshelf",
    "description": "Pixelate your render!",
    "warning": "",
    "doc_url": "",
    "category": "Add Pixelate",
}


import bpy


class PixelatePanel(bpy.types.Panel):
    bl_label = "Pixelate"
    bl_idname = "PIXELATE_PT_MAINPANEL"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Pixelate"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Add a Pixelate Node")
        row = layout.row()
        row.operator("compositor.pixelate_operator")


class PixelateOperator(bpy.types.Operator):
    bl_label = "Add Pixelate"
    bl_idname = "compositor.pixelate_operator"
    
    def execute(self, context):
        bpy.context.scene.use_nodes = True
        bpy.context.scene.node_tree.nodes.clear()
        
    #    add_variables()
        render_layers = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeRLayers")
        render_layers.location.x = -300
        render_layers.location.y = 200
        
        pixelate = bpy.context.scene.node_tree.nodes.new(type="CompositorNodePixelate")
        pixelate.location.x = 300
        pixelate.location.y = 60
        
        viewer = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeViewer")
        viewer.location.x = 800
        viewer.location.y = -100
        
        composite = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeComposite")
        composite.location.x = 800
        composite.location.y = 300
        
        scale_1 = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeScale")
        scale_1.location.x = 100
        scale_1.location.y = 100
        
        #changing scale of scale_1
        bpy.data.scenes["Scene"].node_tree.nodes["Scale"].inputs[1].default_value = 0.1
        bpy.data.scenes["Scene"].node_tree.nodes["Scale"].inputs[2].default_value = 0.1
        
        scale_2 = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeScale")
        scale_2.location.x = 500
        scale_2.location.y = 100
        
        #changing scale of scale_2
        bpy.data.scenes["Scene"].node_tree.nodes["Scale.001"].inputs[1].default_value = 10
        bpy.data.scenes["Scene"].node_tree.nodes["Scale.001"].inputs[2].default_value = 10

        bpy.context.scene.node_tree.links.new(render_layers.outputs["Image"], scale_1.inputs["Image"])
        bpy.context.scene.node_tree.links.new(scale_1.outputs["Image"], pixelate.inputs["Color"])
        bpy.context.scene.node_tree.links.new(pixelate.outputs["Color"], scale_2.inputs["Image"])
        bpy.context.scene.node_tree.links.new(scale_2.outputs["Image"], composite.inputs["Image"])
        bpy.context.scene.node_tree.links.new(scale_2.outputs["Image"], viewer.inputs["Image"])
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(PixelatePanel)
    bpy.utils.register_class(PixelateOperator)


def unregister():
    bpy.utils.unregister_class(PixelatePanel)
    bpy.utils.unregister_class(PixelateOperator)


if __name__ == "__main__":
    register()
