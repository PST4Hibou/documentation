import griffe
from pathlib import Path


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


def _write_function(f, func: griffe.Function, heading_level: int, icon: str = "") -> None:
    hashes = "#" * heading_level
    params = _format_params(func)
    ret = _format_return(func)
    prefix = f"{icon} " if icon else ""
    f.write(f"{hashes} {prefix}`{func.name}({params}){ret}`\n\n")
    if func.docstring:
        f.write(f"{func.docstring.value}\n\n")


def _write_attribute(f, attr: griffe.Attribute, heading_level: int, icon: str = "") -> None:
    hashes = "#" * heading_level
    annotation = f": {attr.annotation}" if attr.annotation else ""
    prefix = f"{icon} " if icon else ""
    f.write(f"{hashes} {prefix}`{attr.name}{annotation}`\n\n")
    if attr.docstring:
        f.write(f"{attr.docstring.value}\n\n")


def write_module_doc(module, out_dir: Path, module_name: str) -> None:
    doc_path = out_dir / Path(*module_name.split(".")).with_suffix(".md")
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    with open(doc_path, "w", encoding="utf-8") as f:
        # Module heading with icon
        f.write(f'# <span class="i-carbon:block-storage" /> {module_name}\n\n')

        if module.docstring:
            f.write(f"{module.docstring.value}\n\n")

        # ── Classes ──────────────────────────────────────────────────────────
        classes = [m for m in module.members.values() if isinstance(m, griffe.Class)]
        if classes:
            f.write("## Classes\n\n")
            for cls in classes:
                f.write(f'### <span class="i-carbon:cube" /> `{cls.name}`\n\n')
                if cls.docstring:
                    f.write(f"{cls.docstring.value}\n\n")

                # __init__ signature
                init = cls.members.get("__init__")
                if init and isinstance(init, griffe.Function):
                    params = _format_params(init)
                    f.write(f"```python\n{cls.name}({params})\n```\n\n")

                # Class members: methods and attributes
                for member in cls.members.values():
                    if member.name.startswith("__") and member.name != "__init__":
                        continue
                    if isinstance(member, griffe.Function) and member.name != "__init__":
                        _write_function(f, member, heading_level=4, icon='<span class="i-carbon:function-2" />')
                    elif isinstance(member, griffe.Attribute):
                        _write_attribute(f, member, heading_level=4, icon='<span class="i-carbon:feature-membership-filled" />')

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
                _write_attribute(f, attr, heading_level=3, icon='<span class="i-carbon:feature-membership-filled" />')

