import griffe
from pathlib import Path


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


def _format_params(func: griffe.Function) -> str:
    parts = []
    for param in func.parameters:
        p = param.name
        if param.annotation:
            p += f": {param.annotation}"
        if param.default:
            p += f" = {param.default}"
        parts.append(p)
    return ", ".join(parts)


def _format_return(func: griffe.Function) -> str:
    return f" -> {func.returns}" if func.returns else ""


def _write_decorators(f, obj) -> None:
    """Write decorators for a function or class if any exist."""
    if not obj.decorators:
        return
    for dec in obj.decorators:
        f.write(f'<span class="i-carbon:at" /> `@{dec.value}`\n\n')


def _write_bases(f, cls: griffe.Class) -> None:
    """Write inherited base classes if any exist."""
    if not cls.bases:
        return
    bases = ", ".join(str(base) for base in cls.bases)
    f.write(f'<span class="i-carbon:branch" /> Inherits from: `{bases}`\n\n')


def _write_function(f, func: griffe.Function, heading_level: int, icon: str = "") -> None:
    hashes = "#" * heading_level
    params = _format_params(func)
    ret = _format_return(func)
    prefix = f"{icon} " if icon else ""
    f.write(f"{hashes} {prefix}`{func.name}({params}){ret}`\n\n")
    _write_decorators(f, func)
    if func.docstring:
        f.write(f"{prettify(func.docstring.value)}\n\n")


def _write_attribute(f, attr: griffe.Attribute, heading_level: int, icon: str = "") -> None:
    hashes = "#" * heading_level
    annotation = f": {attr.annotation}" if attr.annotation else ""
    prefix = f"{icon} " if icon else ""
    f.write(f"{hashes} {prefix}`{attr.name}{annotation}`\n\n")
    if attr.docstring:
        f.write(f"{prettify(attr.docstring.value)}\n\n")


def write_module_doc(module, out_dir: Path, module_name: str) -> None:
    doc_path = out_dir / Path(*module_name.split(".")).with_suffix(".md")
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(f'# <span class="i-carbon:block-storage" /> {module_name}\n\n')

        if module.docstring:
            f.write(f"{prettify(module.docstring.value)}\n\n")

        # ── Classes ──────────────────────────────────────────────────────────
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
                    f.write(f'#### Constructor\n\n')
                    params = _format_params(init)
                    f.write(f"```python\n{cls.name}({params})\n```\n\n")

                methods = [m for m in cls.members.values() if isinstance(m, griffe.Function) and m.name != "__init__" and not m.name.startswith("__")]
                members = [m for m in cls.members.values() if isinstance(m, griffe.Attribute) and m.name != "__init__" and not m.name.startswith("__")]

                if len(methods) != 0:
                    f.write(f'#### Members\n\n')
                    for member in members:
                        _write_attribute(f, member, heading_level=4,
                                         icon='<span class="i-carbon:feature-membership-filled" />')

                if len(methods) != 0:
                    f.write(f'#### Methods\n\n')
                    for member in methods:
                        _write_function(f, member, heading_level=4, icon='<span class="i-carbon:function-2" />')

        # ── Functions ────────────────────────────────────────────────────────
        functions = [m for m in module.members.values() if isinstance(m, griffe.Function)]
        if functions:
            f.write("## Functions\n\n")
            for func in functions:
                _write_function(f, func, heading_level=3, icon='<span class="i-carbon:function-2" />')

        # ── Module-level attributes ───────────────────────────────────────────
        attributes = [m for m in module.members.values() if isinstance(m, griffe.Attribute)]
        if attributes:
            f.write("## Attributes\n\n")
            for attr in attributes:
                _write_attribute(f, attr, heading_level=3,
                                 icon='<span class="i-carbon:feature-membership-filled" />')
