# 🎓 Sentiment & Theme Analysis of High- vs. Low-Performing Schools Using Online Reviews and Discussions

### ADS509 - Applied Large Language Models for Data Science

### ADS-509 Group 3

## 🚀 Live Demo

A working demonstration of this project can be found at **[TJAlytix.streamlit.app](https://tjalytix.streamlit.app)** _(tee-jah-lyticks)_.
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-informational)](https://tjalytix.streamlit.app)

# 💻 Installation

To get started with this project, please clone the repository and navigate
to it:

```{bash}
> git clone https://github.com/junclemente/ads509-final_project.git
> cd ads509-final_project
```

## 🌱 Environment Setup

This project uses a conda environment specified in a YAML file for
reproducibility and consistent development. Ensure you have
[Anaconda](https://www.anaconda.com/download) or
[Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main)
installed.

### Create the Environment

Run the following:

```bash
conda env create -f environment/ads509-streamlit.yaml
```

#### Update the Environment (if needed)

If there are any updates to the environment, you can update the environment
with the following:

```bash
conda env update -f environment/ads509-streamlit.yaml --prune
```

The `--prune` option cleans the environment by removing packages that are
no longer required.

# 👩‍💻👨‍💻 Contributors

- [Amayrani Balbuena](https://github.com/amayranib)
- [Jun Clemente](https://github.com/junclemente)
- [Tanya Ortega](https://github.com/tanyaort)

# 🔀 Development Workflow

- **main** → stable, production-ready branch (protected).
- **develop** → active development branch where new features are merged.
- **feature/\*** → short-lived branches for specific tasks.

### How to Contribute

1. Create a feature branch from `develop`.
2. Commit your changes with clear messages.
3. Open a Pull Request into `develop`.
4. Once reviewed, your changes will be merged into `develop`.
5. At milestones, `develop` is merged into `main`.

👉 See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

# ⚙️ Methods

- Exploratory Data Analysis
- Text Cleaning
- Topic Modeling
- Sentiment Analysis

# 🛠️ Technologies

- Python 3.11+
- Pandas
- NLTK
- Numpy
- Jupyter Notebook
- Matplotlib / Seaborn
- Scikit-learn
- Streamlit
- ChatGPT
- VSCode

# 🎯 Objective

This project looks at how people talk about schools in high-performing vs.
low-performing districts. We're pulling reviews and discussions from
Reddit to see both the overall sentiment (positive or negative)
and the main themes that come up in these conversations.

Our goals are to:

- Run sentiment analysis to check if high-performing schools are talked about more positively compared to low-performing ones.
- Use topic modeling to pull out key themes in each group (like academics, safety, teacher quality, resources).
- Compare the sentiment and themes between high- and low-performing schools to get a clearer picture of how school quality is being perceived online.

# 🗂️ Data Sources

The Reddit API was used to gather the text data sources for processing.

## ⚠️ Disclaimer

This project uses aggregated Reddit data obtained via the [Reddit API](https://www.redditinc.com/policies/data-api-terms).

- No raw Reddit posts or user comments are displayed, stored, or redistributed.
- Only aggregated outputs such as keywords, topics, and sentiment scores are shown.
- All analysis is for **academic, non-commercial research** purposes.

# 📖 References

- [Project Repository](https://github.com/junclemente/ads509-final_project)

# 📽️ Presentations and Projects

- Web Application: [TJAlytics.streamlit.app](https://tjalytix.streamlit.app)
- Project Presentation: Canva.com (TBD)
- Project Repository: [https://github.com/junclemente/ads509-final_project](https://github.com/junclemente/ads509-final_project)

## 🤖 AI Assistance Disclosure

Parts of this project were developed with help from ChatGPT (OpenAI):

- Debugging Python functions and pipeline logic
- Drafting/rewriting docstrings and short notebook summaries
- Creating small code snippets

All generated code and text were reviewed and edited by the authors.
