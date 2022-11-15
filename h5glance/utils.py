"""Helper functions
"""
import h5py

_mapping = {
    h5py.h5f.FileID: "file",
    h5py.h5g.GroupID: "group",
    h5py.h5d.DatasetID: "dataset",
}


def register_h5pyd():
    import h5pyd._hl.objectid as h5pyd_obj
    _mapping[h5pyd_obj.FileID] = "file"
    _mapping[h5pyd_obj.GroupID] = "group"
    _mapping[h5pyd_obj.DatasetID] = "dataset"


def check_class(obj_class):
    """Check registered class"""
    lib = obj_class.__module__.split(".")[0]
    if lib == "h5pyd":
        register_h5pyd()
    else:
        _mapping[obj_class] = None


def get_h5py_kind(obj):
    """Returns the h5py-like kind of an object.

    The result can be `file`, `group`, `dataset` or `None` if the object is not
    an h5py-like object.
    """
    obj_id_class = type(getattr(obj, "id", None))
    if obj_id_class not in _mapping:
        check_class(obj_id_class)
    return _mapping.get(obj_id_class, None)


def is_file(obj):
    """Returns true if the object is a h5py-like file."""
    kind = get_h5py_kind(obj)
    return kind == "file"


def is_dataset(obj):
    """Returns true if the object is a h5py-like dataset."""
    kind = get_h5py_kind(obj)
    return kind == "dataset"


def is_group(obj):
    """Returns true if the object is a h5py-like group."""
    kind = get_h5py_kind(obj)
    return kind in ["file", "group"]


def fmt_shape(shape):
    if shape is None:
        return "empty"
    if shape == ():
        return "scalar"
    return " × ".join(('Unlimited' if n is None else str(n)) for n in shape)
