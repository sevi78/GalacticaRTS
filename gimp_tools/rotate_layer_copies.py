def rotate_layer_copies():
    # Get the currently active image
    image = gimp.image_list()[0]  # Get the first image in the list

    # Get the first layer of the active image
    first_layer = image.layers[0]  # Access the first layer

    # Start an undo group
    pdb.gimp_image_undo_group_start(image)

    # Loop through angles from 0 to 360 in steps of 3 degrees
    for angle in range(0, 360, 3):
        # Create a new layer with the same dimensions and type as the first layer
        new_layer = gimp.Layer(image, "Rotated Layer " + str(angle), first_layer.width, first_layer.height, first_layer.type, 100, NORMAL_MODE)

        # Insert the new layer into the image
        image.add_layer(new_layer, 0)  # Add it at position 0 (top of the stack)

        # Copy the content of the first layer to the new layer
        pdb.gimp_edit_copy(first_layer)  # Copy content of the first layer
        floating_sel = pdb.gimp_edit_paste(new_layer, TRUE)  # Paste into new layer
        pdb.gimp_floating_sel_anchor(floating_sel)  # Anchor the floating selection

        # Rotate the new layer by the current angle (convert degrees to radians)
        angle_in_radians = angle * (3.14159 / 180)

        # Calculate pivot points (center of the new layer)
        center_x = new_layer.width / 2
        center_y = new_layer.height / 2

        # Rotate around center using gimp-item-transform-rotate
        pdb.gimp_item_transform_rotate(new_layer, angle_in_radians, False, center_x, center_y)

    # End undo group
    pdb.gimp_image_undo_group_end(image)

    # Print confirmation
    print("All layers created and rotated.")
