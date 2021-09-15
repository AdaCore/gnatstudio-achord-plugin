# Global functions, needed by widgets accross the board


def __get_instance():
    """Utility function, to retrieve the registered instance of Achord_Integration"""
    try:
        from modules import Module_Metaclass
        from achord_integration import Achord_Integration

        for inst in Module_Metaclass.modules_instances:
            if inst.__class__ == Achord_Integration:
                return inst
    except Exception:
        pass
    return None


def get_achord_connection():
    inst = __get_instance()
    if inst is not None:
        return inst.connection
    return None


def get_achord_elements():
    inst = __get_instance()
    if inst is not None:
        if inst.connection is None:
            return []
        return inst.connection.elements
    return []


def log(msg, add_lf=True):
    inst = __get_instance()
    if inst is None:
        print(msg + ("\n" if add_lf else ""))
    else:
        inst.log(msg, add_lf)
