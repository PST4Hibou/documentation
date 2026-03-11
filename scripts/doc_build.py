import sys
import griffe
from pathlib import Path
from doc import write_module_doc, build_type_registry


def get_import_root(project_root: Path) -> Path:
    """
    Use `src` layout when present, otherwise use project root.
    """
    src_root = project_root / "src"
    return src_root if src_root.is_dir() else project_root


def should_skip(rel_path: Path) -> bool:
    excluded_parts = {"__pycache__", ".git", ".venv", "venv", "node_modules", "tests", "test"}
    return any(part in excluded_parts for part in rel_path.parts)


def file_to_module_name(py_file: Path, import_root: Path) -> str | None:
    """
    Convert a Python file path to an importable module name, relative to import root.
    """
    rel = py_file.relative_to(import_root)

    if should_skip(rel):
        return None

    if py_file.name == "__init__.py":
        parts = list(rel.parent.parts)
    else:
        parts = list(rel.with_suffix("").parts)

    if not parts:
        return None
    if not all(part.isidentifier() for part in parts):
        return None

    return ".".join(parts)


def module_name_to_path(module_name: str, import_root: Path) -> Path | None:
    rel = Path(*module_name.split("."))
    file_path = import_root / rel.with_suffix(".py")
    if file_path.is_file():
        return file_path
    init_path = import_root / rel / "__init__.py"
    if init_path.is_file():
        return init_path
    return None


def find_all_python_modules(import_root: Path) -> list[str]:
    modules: set[str] = set()

    for py_file in import_root.rglob("*.py"):
        module_name = file_to_module_name(py_file, import_root)
        if module_name:
            modules.add(module_name)

    return sorted(modules)


def generate_docs_for_module(module_name: str, out_dir: Path, import_root: Path) -> bool:
    try:
        # Load only the top-level package
        top_level = module_name.split(".")[0]
        elem = griffe.load(top_level, search_paths=[str(import_root)])

        # Navigate to the target submodule using griffe's own resolution
        obj = elem
        for part in module_name.split(".")[1:]:
            if part not in obj.members:
                # griffe loaded the file directly — we're already at the right level
                break
            candidate = obj.members[part]
            # Only descend if it's a module/package, not a class or function
            if isinstance(candidate, (griffe.Module,)):
                obj = candidate
            else:
                break

        write_module_doc(obj, out_dir, module_name)
        print(f"✅ Generated {module_name}")
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"⚠️ Skipped {module_name}: {e!r}")
        return False


def find_readme(project_root: Path) -> Path | None:
    """Find a README file in the project root, case-insensitive."""
    for f in project_root.iterdir():
        if f.is_file() and f.stem.lower() == "readme" and f.suffix.lower() == ".md":
            return f
    return None


def write_index(out_dir: Path, modules: list[str], readme: Path | None = None) -> bool:
    with open(out_dir / "index.md", "w", encoding="utf-8") as f:
        if readme:
            f.write(readme.read_text(encoding="utf-8"))
            f.write("\n\n")
        else:
            f.write('# <span class="i-carbon:api"/> API Reference\n\n')

            for module_name in modules:
                link_path = "/".join(module_name.split("."))
                f.write(f'## <span class="i-carbon:block-storage"/> [{module_name}]({link_path})\n\n')

    return True


def generate(base_path: str, docs_dir: str) -> bool:
    project_root = Path(base_path).resolve()
    import_root = get_import_root(project_root)
    out_dir = Path(docs_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

    module_names = find_all_python_modules(import_root)
    readme = find_readme(project_root)

    print(f"🔍 Project root: {project_root}")
    print(f"🔍 Import root: {import_root}")
    print(f"📁 Found {len(module_names)} module(s)")
    print(f"📄 README: {readme or 'not found'}")

    loaded: dict[str, any] = {}
    for module_name in module_names:
        try:
            top_level = module_name.split(".")[0]
            elem = griffe.load(top_level, search_paths=[str(import_root)])
            obj = elem
            for part in module_name.split(".")[1:]:
                if part not in obj.members:
                    break
                candidate = obj.members[part]
                if isinstance(candidate, griffe.Module):
                    obj = candidate
                else:
                    break
            loaded[module_name] = obj
        except Exception as e:
            print(f"⚠️ Could not load {module_name}: {e!r}")

    build_type_registry(loaded)
    print(f"🔗 Built type registry with {len(loaded)} entries")

    success_count = 0
    for module_name, obj in loaded.items():
        try:
            write_module_doc(obj, out_dir, module_name, all_loaded=loaded)
            print(f"✅ Generated {module_name}")
            success_count += 1
        except Exception as e:
            print(f"⚠️ Skipped {module_name}: {e!r}")

    write_index(out_dir, list(loaded.keys()), readme)

    print(f"\n🎉 Generated {success_count}/{len(module_names)} modules in {out_dir}")
    return success_count == len(module_names)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python doc_build.py <tmp_repo_path> <docs_src_path>")
        sys.exit(1)

    ok = generate(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
