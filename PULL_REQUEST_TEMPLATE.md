# Let's create a PULL_REQUEST_TEMPLATE.md file with a clear structure for contributors.

pr_template_content = """## 📌 Summary

Describe the changes introduced in this Pull Request (PR). Link any related issues.

Fixes # (issue number)

---

## 🔀 Type of Change

- [ ] ✨ Feature (new functionality)
- [ ] 🐛 Bug Fix
- [ ] 📝 Documentation Update
- [ ] ♻️ Refactor (code improvement without behavior change)
- [ ] 🔧 Chore (build, tooling, maintenance)

---

## ✅ Checklist

- [ ] Title & description are clear and descriptive
- [ ] Related issues are linked (if applicable)
- [ ] Added/updated documentation (if needed)
- [ ] Added testing notes or verified locally
- [ ] No large files committed (datasets, models, etc.)
- [ ] Follows [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🖼️ Screenshots / Demo (if applicable)

Attach screenshots, Streamlit demo GIFs, or logs that help reviewers understand your changes.

---

## 🚨 Reviewer Notes

Anything specific reviewers should check carefully? Edge cases, limitations, or follow-ups?
"""

# Save file
pr_template_path = "/mnt/data/PULL_REQUEST_TEMPLATE.md"
with open(pr_template_path, "w") as f:
    f.write(pr_template_content)

pr_template_path
