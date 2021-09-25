from typing import Dict, Union
import pygame_gui
from pygame import Rect

from pygame_gui.core.interfaces.container_interface import IContainerLikeInterface
from pygame_gui.core.interfaces.manager_interface import IUIManagerInterface
from pygame_gui.core.ui_element import ObjectID, UIElement

class Button(pygame_gui.elements.UIButton):
    def __init__(self, relative_rect: Rect, text: str, manager: IUIManagerInterface, container: Union[IContainerLikeInterface, None] = None, tool_tip_text: Union[str, None] = None, starting_height: int = 1, parent_element: UIElement = None, object_id: Union[ObjectID, str, None] = None, anchors: Dict[str, str] = None, allow_double_clicks: bool = False, visible: int = 1,func = None):
        self.func = func
        super().__init__(relative_rect, text, manager, container=container, tool_tip_text=tool_tip_text, starting_height=starting_height, parent_element=parent_element, object_id=object_id, anchors=anchors, allow_double_clicks=allow_double_clicks, visible=visible)
    
    def update(self, time_delta: float):
        if self.check_pressed() and self.func is not None:
            self.func()
        return super().update(time_delta)