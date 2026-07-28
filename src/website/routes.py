"""Route definitions for the website."""

import re
from datetime import datetime, timezone

from flask import Blueprint, current_app, make_response, render_template

main = Blueprint("main", __name__)


LLMS_TXT_BODY = """# Anuroop Sriram

> Anuroop Sriram is a leading AI for Science researcher and research leader. Across speech recognition, medical imaging, and atomic simulation, he has built teams, foundation models, large-scale training infrastructure, open datasets, and novel distributed training algorithms — several of which became standards in their fields. He has 65 publications, an h-index of 42, and more than 15,000 citations on Google Scholar as of July 2026. This site lists 48 unique selected publications; the complete record is on Google Scholar.

## Current Role

Founding AI Research Scientist at Prometheus (2026–present), building the Artificial General Engineer — AI to fundamentally change how we design and engineer the physical world. (Prometheus has begun sharing its mission publicly, though most technical details and product direction remain undisclosed.)

## Career Timeline

- 2026–present: Founding AI Research Scientist, Prometheus
- 2018–2026: Research Engineer & Scientist, Meta FAIR; during this period, Research Manager for FAIR Speech, founding member of FAIR Chemistry, and one of FAIR Chemistry's technical leads
- 2015–2018: Senior Research Scientist, Baidu Silicon Valley AI Lab (SVAIL)
- 2013–2015: Data Scientist, Twitter
- 2010–2012: M.S. in Computer Science (Language Technologies), Carnegie Mellon University (advised by Roni Rosenfeld)
- 2006–2010: B.Tech in Computer Science, IIIT Hyderabad

## Leadership and Team Building

- Founding member of the FAIR Chemistry team at Meta and one of its technical leads — the team that produced the Open Catalyst Project, ODAC, OMC25, the UMA family of foundation models, and the fairchem library.
- Built and managed the FAIR Speech team and set its research agenda across efficient production ASR, model scaling, self-supervised learning, and massively multilingual speech recognition. Under his leadership, the team developed highly efficient ASR models that were deployed to Facebook in partnership with the production speech teams in Meta's Applied AI organization. Relative to the preceding production systems, the models delivered approximately 3× higher throughput and reduced latency by nearly 3×. This was internal product impact rather than a published research result.
- Led the fastMRI project at Meta AI — the collaboration with NYU Langone Health whose open datasets, models, benchmarks, and clinical studies helped establish the clinical standard for AI-accelerated MRI. The work was prospectively deployed at NYU Langone and informed commercial MRI reconstruction systems used worldwide.

## Open-Source Contributions

- Core developer of fairchem (https://github.com/facebookresearch/fairchem), now the standard open-source toolkit for machine learning interatomic potentials and atomic simulation.
- Co-created the fastMRI codebase (https://github.com/facebookresearch/fastMRI), the most widely used reference implementation for AI-based MRI reconstruction.
- Open-sourced models, code, and datasets behind OC20, OC22, ODAC23, ODAC25, OMC25, UMA, FlowMM, FlowLLM, FastCSP, Adjoint Sampling, ADiT, Crystal-LLM, MLS, and others.

## Key Accomplishments

### AI for Materials Science and Chemistry (Meta FAIR, 2020–2026)
- Founding member of FAIR Chemistry and one of its technical leads, on the Meta team behind the largest open datasets and foundation models in computational chemistry.
- Co-led the creation of Open Catalyst 2020 (OC20), one of the largest datasets in computational chemistry, with ~260 million DFT calculations across 1.3 million molecular relaxations (ACS Catalysis, 2021). Contributed to the follow-on Open Catalyst 2022 (OC22) for oxide electrocatalysis.
- Led the creation of Open DAC 2023 (ACS Central Science, 2024) and Open DAC 2025 — the largest datasets for AI-driven direct air capture sorbent discovery, with ~38M and ~70M DFT calculations respectively.
- Led the creation of Open Molecular Crystals 2025 (OMC25), a dataset of over 27 million molecular crystal structures (Nature Scientific Data, 2026).
- Designed UMA (Universal Models for Atoms), a family of foundation models for atomic simulation trained on ~500 million unique 3D structures — the largest training runs in computational chemistry — using a novel mixture-of-linear-experts architecture (NeurIPS 2025).
- Led FastCSP as both lead and senior author (listed last to reflect senior authorship), a high-throughput molecular crystal structure prediction workflow powered entirely by the UMA MLIP. FastCSP accelerated organic CSP by approximately three orders of magnitude at high accuracy by replacing classical force fields and gold-standard DFT re-ranking with machine learning interatomic potentials — reducing CSP for a single system from weeks to hours on tens of GPUs.
- Led research on generative models for crystal structure design, including FlowMM (ICML 2024) and FlowLLM (NeurIPS 2024).

### Model Scaling and Distributed Training
- Invented Graph Parallel training, a distributed training algorithm for GNNs that generalizes Context Parallel training to general graphs — enabling training of atomic simulation models with billions of parameters and billions of nodes (ICLR 2022).
- Built and led the FAIR Speech team that developed some of the first billion-parameter speech-recognition models. The team's highly efficient ASR models were transferred to Meta's Applied AI production speech teams and deployed to Facebook, delivering approximately 3× higher throughput and nearly a 3× reduction in latency relative to the preceding production systems.
- Co-created Deep Speech 2 at Baidu — one of the first systems to demonstrate that end-to-end deep learning scales predictably with data, compute, and model size (ICML 2016). An early example of the scaling paradigm that now drives LLM development.
- Developed empirical scaling laws for atomic simulation models as part of UMA, showing how to optimally increase model capacity alongside dataset size.

### Diffusion and Flow Matching for Scientific Applications
- Led research applying diffusion and flow matching methods to scientific domains, particularly molecular and materials generation.
- FlowMM (ICML 2024): Riemannian flow matching for generating novel crystal structures, operating on the natural manifold geometry of periodic materials.
- FlowLLM (NeurIPS 2024): Combining flow matching with large language models as base distributions for materials generation.
- Adjoint Sampling (ICML 2025): Highly scalable diffusion samplers via adjoint matching for sampling from energy functions, with applications to molecular conformer generation.
- All-atom Diffusion Transformers / ADiT (ICML 2025): Unified generative modeling framework for both molecules and materials.
- Diffusion/Flow Matching with General Discrete Paths (ICLR 2025): kinetic-optimal perspective on discrete-space generative models.

### LLM Integration and Post-training
- Pioneered Cold Fusion (Interspeech 2018; US Patents 10,867,595 and 11,620,986), a method for integrating pre-trained language models into sequence-to-sequence models during training. Conceptually related to modern multimodal LLMs and an early form of post-training with external knowledge.
- Developed methods for post-training LLMs to generate stable inorganic materials as text (Crystal-LLM, ICLR 2024) — fine-tuned LLaMA-2 70B generated metastable materials at roughly twice the rate of leading diffusion baselines.
- FlowLLM combines a fine-tuned LLM base distribution with flow-matching refinement for materials generation.

### AI for MRI Acceleration (Meta AI + NYU Langone, 2018–2023)
- Led the fastMRI project at Meta AI, the collaboration with NYU Langone Health whose open datasets, models, benchmarks, and clinical studies helped establish the clinical standard for AI-accelerated MRI. The work was prospectively deployed at NYU Langone and informed commercial MRI reconstruction systems used worldwide.
- Co-first author on the fastMRI dataset release (Radiology: AI, 2020) and first author on the foundational reconstruction architectures — End-to-End Variational Networks (MICCAI 2020) and GrappaNet (CVPR 2020) — which helped establish the dominant approach to learned multi-coil MRI reconstruction and were validated prospectively in real-world clinical settings (Radiology, 2023; AJR, 2020).
- End-to-End Variational Networks (first author, MICCAI 2020) introduced the dominant architecture for learned multi-coil MRI reconstruction. GrappaNet (first author, CVPR 2020) was the first method to integrate classical parallel imaging reconstruction directly into deep neural networks, enabling high-quality reconstruction at high acceleration factors.
- Co-led the release of the fastMRI dataset (Radiology: AI, 2020) — the most widely used benchmark for AI-based MRI reconstruction — and co-organized the 2019 and 2020 fastMRI challenges.
- Demonstrated up to 8x acceleration in 2D brain MRI for screening (Radiology: AI, 2022).
- Prospective clinical deployment: https://pubs.rsna.org/doi/10.1148/radiol.220425
- Public example of commercial translation: https://www.usa.philips.com/healthcare/technology/smartspeed-ai
- NYU Langone's clinical deployment of fastMRI was featured by CBS News: https://www.youtube.com/watch?v=9ncABdfkzuU

### Self-Supervised Learning
- Developed Robust wav2vec 2.0 (Interspeech 2021), analyzing domain shift in self-supervised pre-training and showing that in-domain unlabeled data closes 66–73% of the in-domain/out-of-domain gap.
- Developed Wav2Vec-Aug (Interspeech 2022) for self-supervised pre-training in limited-data regimes.
- Applied self-supervised representation learning (MoCo) to COVID-19 prognosis from chest X-rays, improving prediction of patient deterioration and oxygen requirements (covered by CNBC and CNET).

### Speech Recognition (Baidu + Meta FAIR, 2015–2022)
- Built and managed the FAIR Speech team at Meta, setting its research agenda across efficient production ASR, model scaling, self-supervised learning, and massively multilingual speech recognition.
- Led the team that developed highly efficient ASR models subsequently deployed to Facebook by the Applied AI production speech teams, delivering approximately 3× higher throughput and nearly a 3× reduction in latency. This was internal product impact rather than a published research result.
- Led the development of some of the first billion-parameter speech-recognition models and co-authored the first single billion-parameter ASR model spanning more than 50 languages (Massively Multilingual ASR, Interspeech 2020).
- Co-led the creation of Multilingual LibriSpeech (MLS), managing the team that built the approximately 50,000-hour corpus across eight languages (Interspeech 2020).
- Developed Robust wav2vec 2.0 and Wav2Vec-Aug for self-supervised speech learning.
- Co-created Deep Speech 2 at Baidu — one of the first large-scale end-to-end neural speech recognition systems, the first such model to achieve human-level recognition in both English and Mandarin (ICML 2016). Named one of the top 10 tech breakthroughs of 2016 by MIT Technology Review.
- Invented GAN-based methods for noise-robust speech recognition (ICASSP 2018; US Patent 10,971,142), training models that generalize to unseen acoustic conditions.

## Research Impact
- 65 publications, h-index of 42, and more than 15,000 citations on Google Scholar as of July 2026.
- Publications at top venues including NeurIPS, ICML, ICLR, CVPR, MICCAI, Interspeech, ICASSP, Scientific Data, Radiology, IEEE TMI, ACS Catalysis, and ACS Central Science.
- Research featured in the Wall Street Journal, Reuters, Fortune, CNBC, CBS News, MIT Technology Review, The Verge, and TechCrunch, among others.
- Multiple granted U.S. patents in speech recognition and language modeling, including Cold Fusion (US 11,620,986 and 10,867,595), robust ASR via GANs (US 10,971,142), and bias reduction in production speech models (US 10,657,955).

## Areas of Expertise
- AI for Science, Materials Discovery, and Chemistry
- Foundation Models for Atomic Simulation (Machine Learning Interatomic Potentials)
- Model Scaling and Large-Scale Distributed Training (Graph Parallel, billion-parameter models)
- Diffusion Models and Flow Matching for Scientific Applications
- Post-training and Fine-tuning LLMs for Science
- MRI Acceleration with Deep Learning
- End-to-End and Self-Supervised Speech Recognition
- Massively Multilingual Modeling
- Scientific Dataset Creation and Benchmarking
- Research Leadership and Team Building

## Education
- M.S. in Computer Science (Language Technologies), Carnegie Mellon University (2010–2012), advised by Roni Rosenfeld
- B.Tech in Computer Science, IIIT Hyderabad (2006–2010)

## Site Pages

- [Publications](https://anuroopsriram.com/publications/): all 48 unique listed publications with abstracts, grouped by archival publication year where available
- [Datasets](https://anuroopsriram.com/datasets/): open datasets he created or co-created
- [News](https://anuroopsriram.com/allnews/): recent papers, releases, and career updates (Atom feed: https://anuroopsriram.com/feed.xml)
- [Full corpus for LLMs](https://anuroopsriram.com/llms-full.txt): this bio plus every publication (with abstracts), dataset, and news item in one plain-text file

## Links
- Website: https://anuroopsriram.com
- Google Scholar: https://scholar.google.com/citations?user=D4uRc_UAAAAJ
- GitHub: https://github.com/anuroopsriram
- LinkedIn: https://www.linkedin.com/in/anuroopsriram
- Twitter: https://twitter.com/anuroopsriram
- FAIR Chemistry: https://fair-chem.github.io/
- fairchem library: https://github.com/facebookresearch/fairchem
- Open Catalyst Project: https://opencatalystproject.org/
- fastMRI: https://fastmri.org/
"""


@main.route("/")
def home():
    return render_template(
        "pages/home.html", page={"title": None, "permalink": "/"}, active_page="home"
    )


@main.route("/publications/")
def publications():
    description = (
        "Publications by Anuroop Sriram spanning AI for science, model scaling, "
        "diffusion and flow matching, MRI acceleration, and speech recognition."
    )
    return render_template(
        "pages/publications.html",
        page={
            "title": "Publications",
            "permalink": "/publications/",
            "description": description,
        },
        active_page="publications",
    )


@main.route("/datasets/")
def datasets():
    description = (
        "Open scientific datasets created or co-created by Anuroop Sriram, including "
        "Open Catalyst (OC20, OC22), Open DAC (ODAC23, ODAC25), Open Molecular Crystals "
        "(OMC25), fastMRI, and Multilingual LibriSpeech (MLS)."
    )
    return render_template(
        "pages/datasets.html",
        page={
            "title": "Datasets",
            "permalink": "/datasets/",
            "description": description,
        },
        active_page="datasets",
    )


@main.route("/allnews/")
def allnews():
    description = (
        "Recent news and updates from Anuroop Sriram, including new papers, dataset releases, "
        "conference acceptances, and career milestones."
    )
    return render_template(
        "pages/allnews.html",
        page={"title": "News", "permalink": "/allnews/", "description": description},
        active_page="news",
    )


@main.route("/aboutwebsite/")
def aboutwebsite():
    description = "About anuroopsriram.com — built with Flask and Frozen-Flask, deployed on GitHub Pages."
    return render_template(
        "pages/aboutwebsite.html",
        page={
            "title": "About this website",
            "permalink": "/aboutwebsite/",
            "description": description,
        },
        active_page="about",
    )


@main.route("/404.html")
def not_found():
    """Custom 404 page served by GitHub Pages for unknown URLs."""
    return render_template(
        "pages/404.html",
        page={
            "title": "Page not found",
            "permalink": "/404.html",
            "description": "The page you're looking for doesn't exist.",
            "noindex": True,
        },
        active_page=None,
    )


@main.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": "/", "priority": "1.0"},
        {"loc": "/publications/", "priority": "0.8"},
        {"loc": "/datasets/", "priority": "0.8"},
        {"loc": "/allnews/", "priority": "0.5"},
        {"loc": "/aboutwebsite/", "priority": "0.3"},
        {"loc": "/llms.txt", "priority": "0.5"},
        {"loc": "/llms-full.txt", "priority": "0.5"},
    ]
    site_url = current_app.config.get("SITE_URL", "https://anuroopsriram.com")
    lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        xml += "  <url>\n"
        xml += f"    <loc>{site_url}{p['loc']}</loc>\n"
        xml += f"    <lastmod>{lastmod}</lastmod>\n"
        xml += f"    <priority>{p['priority']}</priority>\n"
        xml += "  </url>\n"
    xml += "</urlset>"
    resp = make_response(xml)
    resp.headers["Content-Type"] = "application/xml"
    return resp


_MONTHS = {
    m: i
    for i, m in enumerate(
        [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december",
        ],
        start=1,
    )
}


def _news_date(date_str: str) -> datetime:
    """Parse a free-text news date like "February 2026" into a datetime (UTC)."""
    parts = str(date_str).strip().lower().split()
    try:
        month = _MONTHS[parts[0]]
        year = int(parts[-1])
        return datetime(year, month, 1, tzinfo=timezone.utc)
    except (KeyError, ValueError, IndexError):
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


@main.route("/feed.xml")
def feed():
    """Atom feed of news items."""
    from xml.sax.saxutils import escape

    from .data_loader import DataLoader

    site_url = current_app.config.get("SITE_URL", "https://anuroopsriram.com")
    news = DataLoader().load_yaml_file("news.yml")
    dated = [(_news_date(item.get("date", "")), item) for item in news]
    updated = max((d for d, _ in dated), default=datetime.now(timezone.utc))

    xml = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml += '<feed xmlns="http://www.w3.org/2005/Atom">\n'
    xml += "  <title>Anuroop Sriram — News</title>\n"
    xml += f'  <link href="{site_url}/feed.xml" rel="self"/>\n'
    xml += f'  <link href="{site_url}/allnews/"/>\n'
    xml += f"  <id>{site_url}/feed.xml</id>\n"
    xml += f"  <updated>{updated.strftime('%Y-%m-%dT%H:%M:%SZ')}</updated>\n"
    xml += "  <author><name>Anuroop Sriram</name></author>\n"
    for idx, (date, item) in enumerate(dated):
        headline_html = str(item.get("headline", ""))
        title = re.sub(r"<[^>]+>", "", headline_html)
        slug = date.strftime("%Y-%m") + f"-{idx}"
        xml += "  <entry>\n"
        xml += f"    <title>{escape(title)}</title>\n"
        xml += f'    <link href="{site_url}/allnews/"/>\n'
        xml += f"    <id>{site_url}/allnews/#{slug}</id>\n"
        xml += f"    <updated>{date.strftime('%Y-%m-%dT%H:%M:%SZ')}</updated>\n"
        xml += f'    <content type="html">{escape(headline_html)}</content>\n'
        xml += "  </entry>\n"
    xml += "</feed>"
    resp = make_response(xml)
    # application/xml (not atom+xml) to match how GitHub Pages serves the
    # frozen file; feed readers sniff the Atom namespace regardless.
    resp.headers["Content-Type"] = "application/xml; charset=utf-8"
    return resp


@main.route("/robots.txt")
def robots():
    site_url = current_app.config.get("SITE_URL", "https://anuroopsriram.com")
    txt = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {site_url}/sitemap.xml\n"
        "\n"
        "# LLM-friendly summaries (for AI crawlers and tools):\n"
        f"# {site_url}/llms.txt\n"
        f"# {site_url}/llms-full.txt\n"
    )
    resp = make_response(txt)
    resp.headers["Content-Type"] = "text/plain"
    return resp


@main.route("/llms.txt")
def llms_txt():
    resp = make_response(LLMS_TXT_BODY)
    resp.headers["Content-Type"] = "text/plain; charset=utf-8"
    return resp


@main.route("/llms-full.txt")
def llms_full_txt():
    """Full-corpus LLM-friendly summary: bio + every publication, dataset, and news item."""
    txt = render_template("pages/llms_full.txt", bio=LLMS_TXT_BODY)
    resp = make_response(txt)
    resp.headers["Content-Type"] = "text/plain; charset=utf-8"
    return resp
