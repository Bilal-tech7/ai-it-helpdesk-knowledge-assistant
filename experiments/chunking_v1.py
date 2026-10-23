print("STEP 10 RUNNING")

with open("knowledge_base/password-reset.md", encoding="utf-8") as f:
    text = f.read()

sections = text.split("\n## ")

print("Number of pieces:", len(sections))
for section in sections:
    print("-", section.split("\n")[0])