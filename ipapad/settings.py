# -*- coding: utf-8 -*-
"""Tools for the management of program settings"""

import json
import os


class SettingsManager:
    """Stores and represents program settings"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, use_defaults=True):
        # Default values
        if use_defaults:
            self.mw_height = 500
            self.mw_width = 800
            self.use_tabs = True
            self.show_toolbar = True
            self.show_pul_cons = True
            self.show_npul_cons = True
            self.show_vowels = True
            self.show_others = True
            self.show_suprasegs = True
            self.show_diacs = True
            self.show_tones = True
            self.type_ipa = True

    def load_from_file(self, path):
        """Loads settings from JSON file"""
        with open(path, "r", encoding="utf-8") as file:
            attrs = json.load(file)
        for a_name, a_value in attrs.items():
            setattr(self, a_name, a_value)

    def save_to_file(self, path):
        """Saves settings to JSON file"""
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.__dict__, file, indent=2)

    @staticmethod
    def get_user_path(app_name):
        app_name = app_name.replace(" ", "_")
        if os.name == "nt" and os.getenv("APPDATA", False):
            path = os.path.join(os.getenv("APPDATA"), app_name)
        else:
            app_name = app_name.lower()
            path = os.path.join(os.path.expanduser("~"), f".{app_name}")
        if not os.path.exists(path):
            os.mkdir(path)
        return path
