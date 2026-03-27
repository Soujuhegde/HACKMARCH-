with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
indent_mode = False

for line in lines:
    stripped = line.strip()
    # Check if we are starting a with tabX: block
    if stripped in ["with tab2:", "with tab3:", "with tab4:"]:
        tab_name = stripped.split(' ')[1][:-1]
        out.append(f"if {tab_name} is not None:\\n")
        out.append(f"    with {tab_name}:\\n")
        indent_mode = True
    elif indent_mode and stripped.startswith("# ════"):
        # We hit the next section divider, stop indenting
        indent_mode = False
        out.append(line)
    else:
        # If we are inside the tab block, indent the line by 4 spaces
        if indent_mode and line.strip('\r\n') != "":
            out.append("    " + line)
        elif indent_mode and line.strip('\r\n') == "":
            out.append(line) # preserve empty lines without adding spaces just in case
        else:
            out.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(out)
