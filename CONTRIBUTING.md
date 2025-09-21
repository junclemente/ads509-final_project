# Contributing Guidelines

Thanks for contributing! Please follow these guidelines so we can all work smoothly.

---

## 📌 Branching Model

We use a simple **main / develop / feature** workflow:

- **main**
  - Production-ready branch.
  - Protected: do not commit or push directly.
  - Updated only via Pull Requests (PRs) from `develop`.

- **develop**
  - Active integration branch.
  - All features and fixes are merged here first.
  - May be lightly protected (optional reviews).

- **feature/***
  - Branches created off `develop`.
  - Examples:
    - `feature/topic-modeling`
    - `fix/readme-typo`
    - `docs/add-usage-guide`
  - Deleted after merge.

---

## 🔀 Workflow

1. Always start by updating your local `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Create a feature branch:
   ```bash
   git checkout -b feature/<short-name>
   ```

3. Make your changes. Stage and commit often:
   ```bash
   git add .
   git commit -m "feat: add baseline topic modeling with NMF"
   ```

4. Push your branch:
   ```bash
   git push -u origin feature/<short-name>
   ```

5. Open a Pull Request (PR) into `develop`.
   - At least one teammate should review.
   - Use **Squash and Merge** unless otherwise agreed.

6. When we reach a stable milestone:
   - Open a PR from `develop` → `main`.
   - Tag the commit (e.g., `v0.1.0`) for that release.

---

## ✅ Pull Request Checklist

- Clear title & description of changes.
- Link to related issues (if any).
- Include screenshots/GIFs for UI changes (e.g., Streamlit).
- Add testing notes if applicable.
- No large data files committed (use `/data/.gitignore`).

---

## ✍️ Commit Style

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code change that doesn’t add features or fix bugs
- `chore:` — build, tooling, maintenance

Example:
```bash
git commit -m "feat: add dropout risk prediction model with XGBoost"
```

---

## 🚀 Releases

1. Merge `develop` → `main` via PR.
2. Create a version tag:
   ```bash
   git tag -a v0.1.0 -m "Milestone: baseline classifier + Streamlit app"
   git push origin v0.1.0
   ```

---

## ⚠️ Data & Large Files

- Keep raw/processed data out of Git.
- Use `/data/.gitignore` for local datasets.
- If needed, use Git LFS for small artifacts.


---

## 🎨 Common Emojis for Commits & PRs

To keep messages consistent and easy to scan, feel free to use these emoji shortcodes:

| Emoji | Code | Typical Use |
|-------|------|--------------|
| ✨ | `:sparkles:` | New feature |
| 🐛 | `:bug:` | Bug fix |
| 📝 | `:memo:` | Documentation |
| ♻️ | `:recycle:` | Refactor code |
| 🔧 | `:wrench:` | Tooling / configuration |
| 🚨 | `:rotating_light:` | Tests / warnings |
| ✅ | `:white_check_mark:` | Passing tests / completed checklist |
| ❌ | `:x:` | Removed code or failing checks |
| ⚡ | `:zap:` | Performance improvements |
| 🔒 | `:lock:` | Security fix |
| 📦 | `:package:` | New release / dependencies |
| 📊 | `:bar_chart:` | Data / analytics work |
| 🎉 | `:tada:` | Project start / release milestone |

👉 Example commit:
```bash
git commit -m "feat: ✨ add dropout prediction model with XGBoost"
