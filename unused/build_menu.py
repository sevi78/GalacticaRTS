import pygame

from source.gui.widgets.buttons.button import Button
from source.gui.widgets.buttons.button_array import ButtonArray
from source.multimedia_library.images import images, pictures_path
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups


class BuildMenu:
    def __init__(self, config):
        self.build_menu_visible = False
        self.build_menu_widgets = []
        self.build_menu_widgets_buildings = {"energy": [],
                                             "food": [],
                                             "minerals": [],
                                             "water": [],
                                             "city": [],
                                             "technology": []
                                             }
        self.config = config

    def create_build_menu(self):
        """
        this monster creates the buildmenu; an overview over all buildable things
        :return:
        """
        # width (relative dynamic: use colon_size_x to adjust
        x = 0
        colon_size_x = self.config["colon_size_x"]
        start_x = 0 - colon_size_x / 2

        # height (dynamic)
        build_menu_height = 702  # 732-30 muss durch 3 teilbar sein
        start_y = 60
        y = 0
        row_size_y = 30

        # font sizes
        price_font_size = self.config["price_font_size"]

        # text colors
        price_color_cost = self.config["price_color_cost"]
        price_color_win = self.config["price_color_win"]

        # image sizes
        price_image_size = self.config["price_image_size"]

        # colons
        colons = self.config["colons"]

        # first row(titles)
        for colon in colons:
            if colon == "resource":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x / 2), y=start_y,
                    width=int(colon_size_x / 2),
                    height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)
            elif colon == "building":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x), y=start_y, width=int(colon_size_x / 2),
                    height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)
            elif colon == "price":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x + colon_size_x / 2), y=start_y,
                    width=colon_size_x, height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)
            elif colon == "production":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x + colon_size_x / 2 + colon_size_x),
                    y=start_y,
                    width=colon_size_x, height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)

            button.disable()
            self.build_menu_widgets.append(button)

        # next row
        y += start_y + row_size_y
        y_hold = y
        x = start_x
        row_size_y = build_menu_height / 6  # this might be wrong

        # resource icons (first colon)
        for r in self.resources:
            colon_name = Button(win=self.win, x=x + colon_size_x / 2, y=y, width=colon_size_x / 2,
                height=int(row_size_y),
                text=r + ": ",
                image=pygame.transform.scale(images[pictures_path]["resources"][r + "_25x25.png"],
                    (50, 50)),
                borderThickness=1, imageHAlign="left", textHAlign="right", layer=9)

            y += row_size_y
            colon_name.disable()
            self.build_menu_widgets.append(colon_name)

        # hold y for later use, remove "resource", no need anymore, only building, price and production is needed
        y = y_hold
        x += colon_size_x
        colons.remove("resource")

        # dynamic creation of all widgets (resource, building, price, production) with arrays for every row
        ry = 0
        for r in self.resources:
            for colon in colons:
                if colon == "building":
                    # print ("build_menu_ ", r, self.buildings[r][0])
                    buildings_array = ButtonArray(win=self.win, x=x, y=y + ry,
                        width=colon_size_x / 2,
                        height=int(row_size_y),
                        shape=(1, 3),
                        border=1,
                        texts=self.buildings[r],
                        images=[images[pictures_path]["buildings"][
                                    self.buildings[r][0] + "_25x25.png"],
                                images[pictures_path]["buildings"][
                                    self.buildings[r][1] + "_25x25.png"],
                                images[pictures_path]["buildings"][
                                    self.buildings[r][2] + "_25x25.png"]],

                        textHAligns=("right", "right", "right"),
                        imageHAligns=("left", "left", "left"),
                        bottomBorder=0,
                        names=[self.buildings[r][0], self.buildings[r][1],
                               self.buildings[r][2]],
                        tooltips=["not set", "not set", "not set"],
                        parents=[self, self, self],
                        propertys=[r, r, r],
                        layers=[9, 9, 9])
                    # onClicks=[lambda: self.build(self.buildings[r][0]),
                    #           lambda: self.build(self.buildings[r][1]),
                    #           lambda: self.build(self.buildings[r][2])])
                    self.build_menu_widgets.append(buildings_array)

                    for button in buildings_array.getButtons():
                        self.build_menu_widgets_buildings[r].append(button)

                if colon == "price":
                    # set the colors based on the values: orange for negative values, green for positive values
                    price_colors = [0, 0, 0, 0]
                    for i in self.buildings[r]:
                        if self.prices[i]["water"] > 0:
                            price_colors[0] = price_color_cost
                        if self.prices[i]["energy"] > 0:
                            price_colors[1] = price_color_cost
                        if self.prices[i]["food"] > 0:
                            price_colors[2] = price_color_cost
                        if self.prices[i]["minerals"] > 0:
                            price_colors[3] = price_color_cost

                        price_array = ButtonArray(win=self.win, x=x + colon_size_x - colon_size_x / 2, y=y + ry,
                            width=colon_size_x,
                            height=int(row_size_y / 3),
                            shape=(4, 1), border=1,
                            texts=[str(self.prices[i]["water"]),
                                   str(self.prices[i]["energy"]),
                                   str(self.prices[i]["food"]),
                                   str(self.prices[i]["minerals"])],
                            font_sizes=[price_font_size, price_font_size, price_font_size,
                                        price_font_size],

                            images=[pygame.transform.scale(
                                images[pictures_path]["resources"]["water" + "_25x25.png"],
                                price_image_size),
                                pygame.transform.scale(
                                    images[pictures_path]["resources"][
                                        "energy" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    images[pictures_path]["resources"][
                                        "food" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    images[pictures_path]["resources"][
                                        "minerals" + "_25x25.png"], price_image_size)],

                            onClicks=(
                                lambda: print("no function"), lambda: print("no function"),
                                lambda: print("no function"),
                                lambda: print("no function")),

                            imageHAligns=("left", "left", "left", "left"),
                            textColours=price_colors,
                            layers=[9, 9, 9, 9])

                        self.build_menu_widgets.append(price_array)
                        for pb in price_array.getButtons():  pb.disable()
                        y += row_size_y / 3
                    y -= row_size_y

                if colon == "production":
                    price_colors = [0, 0, 0, 0]
                    for i in self.buildings[r]:
                        if self.production[i]["water"] > 0:
                            price_colors[0] = price_color_win
                        if self.production[i]["energy"] > 0:
                            price_colors[1] = price_color_win
                        if self.production[i]["food"] > 0:
                            price_colors[2] = price_color_win
                        if self.production[i]["minerals"] > 0:
                            price_colors[3] = price_color_win

                        if self.production[i]["water"] < 0:
                            price_colors[0] = price_color_cost
                        if self.production[i]["energy"] < 0:
                            price_colors[1] = price_color_cost
                        if self.production[i]["food"] < 0:
                            price_colors[2] = price_color_cost
                        if self.production[i]["minerals"] < 0:
                            price_colors[3] = price_color_cost

                        production_array = ButtonArray(win=self.win,
                            x=x + colon_size_x + colon_size_x - colon_size_x / 2, y=y + ry,
                            width=colon_size_x,
                            height=int(row_size_y / 3),
                            shape=(4, 1), border=1,
                            texts=[str(self.production[i]["water"]),
                                   str(self.production[i]["energy"]),
                                   str(self.production[i]["food"]),
                                   str(self.production[i]["minerals"])],
                            font_sizes=[price_font_size, price_font_size, price_font_size,
                                        price_font_size],

                            images=[pygame.transform.scale(
                                images[pictures_path]["resources"][
                                    "water" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    images[pictures_path]["resources"][
                                        "energy" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    images[pictures_path]["resources"][
                                        "food" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    images[pictures_path]["resources"][
                                        "minerals" + "_25x25.png"], price_image_size)],
                            onClicks=(lambda: print(1), lambda: print(2), lambda: print(3),
                                      lambda: print(4)),

                            imageHAligns=("left", "left", "left", "left"),
                            textColours=price_colors,
                            layers=[9, 9, 9, 9]
                            )

                        self.build_menu_widgets.append(production_array)
                        for i in production_array.getButtons():  i.disable()
                        y += row_size_y / 3

                    # reset y for next colon
                    y -= row_size_y

            # set ry (resource position y ) for next resource
            ry += row_size_y

    def open_build_menu(self):
        if not self.selected_planet:
            return

        self.build_menu_visible = True

        # disable all object below
        for i in self.build_menu_widgets:
            i.show()
            try:
                for button in i.getButtons():
                    button.show()
            except:
                pass

        for i in self.game_objects:
            i.disable()
        for i in sprite_groups.planets:
            i.disable()

        for i in self.ships:
            i.disable()

        # disable button is not possible to build it
        for key, value in self.build_menu_widgets_buildings.items():
            for button in self.build_menu_widgets_buildings[key]:
                if button.property not in self.selected_planet.possible_resources:
                    # button.disable()
                    button.hide()

                else:
                    # button.enable()
                    button.show()

    def close_build_menu(self):
        self.build_menu_visible = False

        if self.build_menu_widgets[0].isVisible():

            # to_hide = [1, 3]
            # for i in WidgetHandler.WidgetHandler.getWidgets():
            #     if i.layer in to_hide:
            #         i.show()

            for i in self.build_menu_widgets:
                i.hide()
                try:
                    for button in i.getButtons():
                        button.hide()
                except:
                    pass

            for i in self.game_objects:
                i.enable()

            for i in sprite_groups.planets:
                i.enable()

            for i in self.ships:
                i.enable()


# Configuration file or data structure
config = {
    "colon_size_x": 466,
    "price_font_size": 20,
    "price_color_cost": pygame.color.THECOLORS["orange"],
    "price_color_win": pygame.color.THECOLORS["green"],
    "price_image_size": (16, 16),
    "colons": ["resource", "building", "price", "production"]
    }
