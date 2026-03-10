import griffe
from pathlib import Path
import re


# Global type registry: type name -> relative doc link
# e.g. {"AudioWorker": "modules/audio/worker", "DanteADCDevice": "modules/audio/devices/dante/models"}
_TYPE_REGISTRY: dict[str, str] = {}


# Fallback docs for well-known packages
# Maps module/type name prefixes to their base API doc URL
_EXTERNAL_DOCS: dict[str, str] = {
    # Python stdlib
    "Path": "https://docs.python.org/3/library/pathlib.html#pathlib.Path",
    "Dict": "https://docs.python.org/3/library/typing.html#typing.Dict",
    "List": "https://docs.python.org/3/library/typing.html#typing.List",
    "Tuple": "https://docs.python.org/3/library/typing.html#typing.Tuple",
    "Set": "https://docs.python.org/3/library/typing.html#typing.Set",
    "Optional": "https://docs.python.org/3/library/typing.html#typing.Optional",
    "Union": "https://docs.python.org/3/library/typing.html#typing.Union",
    "Any": "https://docs.python.org/3/library/typing.html#typing.Any",
    "Callable": "https://docs.python.org/3/library/typing.html#typing.Callable",
    "Type": "https://docs.python.org/3/library/typing.html#typing.Type",
    "ClassVar": "https://docs.python.org/3/library/typing.html#typing.ClassVar",
    "Final": "https://docs.python.org/3/library/typing.html#typing.Final",
    "Literal": "https://docs.python.org/3/library/typing.html#typing.Literal",
    "Awaitable": "https://docs.python.org/3/library/typing.html#typing.Awaitable",
    "Coroutine": "https://docs.python.org/3/library/typing.html#typing.Coroutine",
    "AsyncIterator": "https://docs.python.org/3/library/typing.html#typing.AsyncIterator",
    "Iterator": "https://docs.python.org/3/library/typing.html#typing.Iterator",
    "Generator": "https://docs.python.org/3/library/typing.html#typing.Generator",
    "Thread": "https://docs.python.org/3/library/threading.html#threading.Thread",
    "Process": "https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process",
    "Queue": "https://docs.python.org/3/library/queue.html#queue.Queue",
    "ABC": "https://docs.python.org/3/library/abc.html#abc.ABC",
    "abstractmethod": "https://docs.python.org/3/library/abc.html#abc.abstractmethod",
    "dataclass": "https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass",
    "datetime": "https://docs.python.org/3/library/datetime.html#datetime.datetime",
    "Enum": "https://docs.python.org/3/library/enum.html#enum.Enum",
    "property": "https://docs.python.org/3/library/functions.html#property",
    "staticmethod": "https://docs.python.org/3/library/functions.html#staticmethod",
    "classmethod": "https://docs.python.org/3/library/functions.html#classmethod",
    "logging": "https://docs.python.org/3/library/logging.html",
    "Logger": "https://docs.python.org/3/library/logging.html#Logger",
    "contextlib": "https://docs.python.org/fr/3/library/contextlib.html",
    "contextmanager": "https://docs.python.org/fr/3/library/contextlib.html#contextmanager",
    # Numpy
    "np": "https://numpy.org/doc/stable/reference/index.html",
    "ndarray": "https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html",
    # Torch
    "torch": "https://pytorch.org/docs/stable/index.html",
    "Tensor": "https://pytorch.org/docs/stable/tensors.html",
    # Built-in types
    "int": "https://docs.python.org/3/library/functions.html#int",
    "float": "https://docs.python.org/3/library/functions.html#float",
    "complex": "https://docs.python.org/3/library/functions.html#complex",
    "str": "https://docs.python.org/3/library/stdtypes.html#str",
    "bool": "https://docs.python.org/3/library/functions.html#bool",
    "bytes": "https://docs.python.org/3/library/stdtypes.html#bytes",
    "bytearray": "https://docs.python.org/3/library/stdtypes.html#bytearray",
    "memoryview": "https://docs.python.org/3/library/stdtypes.html#memoryview",
    "list": "https://docs.python.org/3/library/stdtypes.html#list",
    "tuple": "https://docs.python.org/3/library/stdtypes.html#tuple",
    "set": "https://docs.python.org/3/library/stdtypes.html#set",
    "frozenset": "https://docs.python.org/3/library/stdtypes.html#frozenset",
    "dict": "https://docs.python.org/3/library/stdtypes.html#dict",
    "type": "https://docs.python.org/3/library/functions.html#type",
    "object": "https://docs.python.org/3/library/functions.html#object",
    "None": "https://docs.python.org/3/library/constants.html#None",
    "NoneType": "https://docs.python.org/3/library/constants.html#None",
    "NotImplemented": "https://docs.python.org/3/library/constants.html#NotImplemented",
    "Ellipsis": "https://docs.python.org/3/library/constants.html#Ellipsis",
}


def register_external_type(name: str, url: str) -> None:
    """Allow callers to add extra external type mappings at runtime."""
    _EXTERNAL_DOCS[name] = url


def build_type_registry(modules: dict[str, any]) -> None:
    """
    Populate _TYPE_REGISTRY from all loaded griffe modules.
    Call this once after all modules are loaded, before writing docs.
    """
    global _TYPE_REGISTRY
    for module_name, module in modules.items():
        link = "/".join(module_name.split("."))
        # Register classes
        for member in module.members.values():
            if isinstance(member, griffe.Class):
                _TYPE_REGISTRY[member.name] = f"/{link}#{member.name.lower()}"
            # Register type aliases (module-level Attribute with a class value)
            elif isinstance(member, griffe.Attribute):
                _TYPE_REGISTRY[member.name] = f"/{link}#{member.name.lower()}"


def _resolve_type(name: str) -> str | None:
    """Return a doc URL for a type name, checking internal registry then external."""
    if name in _TYPE_REGISTRY:
        return _TYPE_REGISTRY[name]
    if name in _EXTERNAL_DOCS:
        return _EXTERNAL_DOCS[name]
    return None


def _linkify_type(type_str: str) -> str:
    if not type_str:
        return type_str

    def replace_match(m: re.Match) -> str:
        name = m.group(0)
        url = _resolve_type(name)
        if url:
            return f"[{name}]({url})"
        return name

    return re.sub(r'\b([a-zA-Z][a-zA-Z0-9_]*)\b', replace_match, type_str)


def _get_link_for_type(type_str: str) -> str:
    """Return a single URL for the base name of a type/decorator, or empty string."""
    if not type_str:
        return ""
    # Only extract the leading identifier, ignore call args like ()
    base_name = re.match(r'([a-zA-Z][a-zA-Z0-9_]*)', type_str.strip())
    if base_name:
        return _resolve_type(base_name.group(1)) or ""
    return ""


def _format_params(func: griffe.Function) -> str:
    parts = []
    for param in func.parameters:
        p = f"`{param.name}`"
        if param.annotation:
            p += f": {_linkify_type(str(param.annotation))}"
        if param.default:
            p += f" = `{param.default}`"
        parts.append(p)
    return ", ".join(parts)


def _format_return(func: griffe.Function) -> str:
    if func.returns:
        return f" -> {_linkify_type(str(func.returns))}"
    return ""


def prettify(md):
    lines = md.splitlines()

    def process_line(line):
        leading_spaces = len(line) - len(line.lstrip())
        content = line.lstrip()

        if ':' in content and content.split(':')[0].strip():
            if leading_spaces == 0:
                original = content.split(':', 1)[0].strip()
                rest = content.split(':', 1)[1] if len(content.split(':')) > 1 else ''
                content = f"**{original}:** {rest}"
            else:
                original = content.split(':', 1)[0].strip()
                rest = content.split(':', 1)[1] if len(content.split(':')) > 1 else ''
                content = f"*{original}:* {rest}"

        return content

    bold_lines = [process_line(line) for line in lines]
    return ' \\\n'.join(bold_lines)


def _write_decorators(f, obj) -> None:
    if not obj.decorators:
        return
    for dec in obj.decorators:
        value = str(dec.value)
        link = _get_link_for_type(value)
        if link:
            f.write(f'<a href="{link}">`@{value}`</a>\n\n')
        else:
            f.write(f'`@{value}`\n\n')


def _write_bases(f, cls: griffe.Class) -> None:
    if not cls.bases:
        return
    bases = ", ".join(_linkify_type(str(base)) for base in cls.bases)
    f.write(f'<span class="i-carbon:branch" /> Inherits from: {bases}\n\n')


def _write_function(f, func: griffe.Function, heading_level: int, icon: str = "") -> None:
    hashes = "#" * (heading_level+1)
    prefix = f"{icon} " if icon else ""

    # Build params with types outside backticks
    param_parts = []
    for param in func.parameters:
        p = f"`{param.name}`"
        if param.annotation:
            p += f": {_linkify_type(str(param.annotation))}"
        if param.default:
            p += f" = `{param.default}`"
        param_parts.append(p)
    params_str = ", ".join(param_parts)

    # Return type outside backticks
    ret_str = ""
    if func.returns:
        ret_str = f" → {_linkify_type(str(func.returns))}"

    f.write(f"{hashes} {prefix}`{func.name}`({params_str}){ret_str}\n\n")
    _write_decorators(f, func)
    if func.docstring:
        f.write(f"{prettify(func.docstring.value)}\n\n")


def _write_attribute(f, attr: griffe.Attribute, heading_level: int, icon: str = "") -> None:
    hashes = "#" * (heading_level+1)
    prefix = f"{icon} " if icon else ""

    annotation = ""
    if attr.annotation:
        annotation = f": {_linkify_type(str(attr.annotation))}"

    f.write(f"{hashes} {prefix}`{attr.name}`{annotation}\n\n")
    if attr.docstring:
        f.write(f"{prettify(attr.docstring.value)}\n\n")


def write_module_doc(module, out_dir: Path, module_name: str) -> None:
    doc_path = out_dir / Path(*module_name.split(".")).with_suffix(".md")
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(f'# <span class="i-carbon:block-storage" /> {module_name}\n\n')

        if module.docstring:
            f.write(f"{prettify(module.docstring.value)}\n\n")

        classes = [m for m in module.members.values() if isinstance(m, griffe.Class)]
        if classes:
            f.write("## Classes\n\n")
            for cls in classes:
                f.write(f'### <span class="i-carbon:cube" /> `{cls.name}`\n\n')
                _write_decorators(f, cls)
                _write_bases(f, cls)
                if cls.docstring:
                    f.write(f"{prettify(cls.docstring.value)}\n\n")

                init = cls.members.get("__init__")
                if init and isinstance(init, griffe.Function):
                    f.write('#### Constructor\n\n')
                    params = _format_params(init)
                    f.write(f"\n###### `{cls.name}`({params})\n\n")

                methods = [m for m in cls.members.values() if isinstance(m, griffe.Function) and m.name != "__init__" and not m.name.startswith("__")]
                members = [m for m in cls.members.values() if isinstance(m, griffe.Attribute) and not m.name.startswith("__")]

                if members:
                    f.write('#### Members\n\n')
                    for member in members:
                        _write_attribute(f, member, heading_level=5,
                                         icon='<span class="i-carbon:feature-membership-filled" />')

                if methods:
                    f.write('#### Methods\n\n')
                    for method in methods:
                        _write_function(f, method, heading_level=5,
                                        icon='<span class="i-carbon:function-2" />')

        functions = [m for m in module.members.values() if isinstance(m, griffe.Function)]
        if functions:
            f.write("## Functions\n\n")
            for func in functions:
                _write_function(f, func, heading_level=3, icon='<span class="i-carbon:function-2" />')

        attributes = [m for m in module.members.values() if isinstance(m, griffe.Attribute)]
        if attributes:
            f.write("## Attributes\n\n")
            for attr in attributes:
                _write_attribute(f, attr, heading_level=3,
                                 icon='<span class="i-carbon:feature-membership-filled" />')
