from pygame import Rect, Vector2

from source.handlers.file_handler import write_file, load_file


class QTSaveLoad:
    def __init__(self, qt_game_object_manager):
        self.qt_game_object_manager = qt_game_object_manager

    def load(self, filename, folder):
        file = load_file(filename, folder)
        self.qt_game_object_manager.game.universe_factory.delete_universe()
        self.qt_game_object_manager.game.universe_factory.create_universe_from_data(file)

    def rect_to_dict(self, rect):
        return {
            'x': rect.x,
            'y': rect.y,
            'width': rect.width,
            'height': rect.height
            }

    def object_to_dict(self, obj):
        if hasattr(obj, '__dict__'):
            obj_dict = obj.__dict__.copy()
            for key, value in obj_dict.items():
                if isinstance(value, Rect):
                    obj_dict[key] = self.rect_to_dict(value)
                elif isinstance(value, Vector2):
                    obj_dict[key] = {'x': value.x, 'y': value.y}
                # elif isinstance(value, (QTImage, QTFlickeringStar, QTPulsatingStar, QTGif, QTMovingImage)):
                #     obj_dict[key] = self.object_to_dict(value)
                elif key in ['target', 'orbit_object'] and value is not None:
                    obj_dict[key] = value.id
                elif hasattr(value, '__dict__'):
                    obj_dict[key] = self.object_to_dict(value)
            return obj_dict
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)

    def save(self, data: list[object]):
        converted_data = {f"object_{i}": self.object_to_dict(obj) for i, obj in enumerate(data)}

        print(f"converted_data: {type(converted_data)}")

        # pprint (converted_data)
        # json_data = json.dumps(converted_data, indent=4).encode('utf-8')
        write_file("test.json", "qt_database", converted_data)
