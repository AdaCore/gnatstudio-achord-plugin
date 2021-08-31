# Global functions, needed by widgets accross the board
from modules import Module_Metaclass


def __get_instance():
    """Utility function, to retrieve the registered instance of Achord_Integration"""
    from achord_integration import Achord_Integration

    for inst in Module_Metaclass.modules_instances:
        if inst.__class__ == Achord_Integration:
            return inst
    return None


def get_achord_connection():
    inst = __get_instance()
    if inst is not None:
        return inst.connection
    return None
