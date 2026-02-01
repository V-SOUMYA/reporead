def build_project_structure(folders):
    structure = {
        "documentation": [],
        "examples": [],
        "tests": [],
        "configuration": [],
        "other": []
    }

    for folder in folders:
        if folder.startswith("docs"):
            structure["documentation"].append(folder)
        elif folder.startswith("examples"):
            structure["examples"].append(folder)
        elif folder.startswith("tests"):
            structure["tests"].append(folder)
        elif folder.startswith(".github"):
            structure["configuration"].append(folder)
        else:
            structure["other"].append(folder)

    # remove empty groups
    return {k: v for k, v in structure.items() if v}
