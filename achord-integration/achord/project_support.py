# Various utilities for project support

import os


def make_path_project_relative(filename):
    try:
        import GPS

        project_dir = os.path.dirname(GPS.Project.root().filename())
        return os.path.relpath(filename, start_dir=project_dir)
    except Exception:
        return os.path.basename(filename)
