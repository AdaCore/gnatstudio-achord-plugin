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


testsuite_connection = None


def testsuite_set_achord_connection(m):
    """Used for the testsuite: set a connection"""
    global testsuite_connection
    testsuite_connection = m


def get_achord_connection():
    inst = __get_instance()
    if inst is not None:
        return inst.connection

    if testsuite_connection is not None:
        return testsuite_connection

    return None


def get_achord_link_types():
    inst = __get_instance()
    if inst is not None:
        if inst.connection is None:
            return []
        return inst.connection.link_types
    return []


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
        print(msg, end="\n" if add_lf else "")
    else:
        inst.log(msg, add_lf)
