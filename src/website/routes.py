"""Route definitions for the website."""

from datetime import datetime

from flask import Blueprint, render_template, make_response, current_app

main = Blueprint('main', __name__)


LLMS_TXT_BODY = """# Anuroop Sriram

> Anuroop Sriram is a leading AI for Science researcher. Across speech recognition, medical imaging, and atomic simulation, he has built foundation models, large-scale training infrastructure, and novel distributed training algorithms — several of which became the standard in their field. He has 65 publications, an h-index of 42, and nearly 15,000 citations on Google Scholar.

## Current Role

Founding AI Research Scientist at Prometheus (2026–present), building AI to fundamentally change how we design and engineer the physical world. (Prometheus is in stealth; specific technical details and product direction have not been publicly disclosed.)

## Career Timeline

- 2026–present: Founding AI Research Scientist, Prometheus
- 2018–2026: Research Engineer & Scientist, Meta FAIR (Research Manager for FAIR Speech; founding member of FAIR Chemistry and one of its technical leads)
- 2015–2018: Senior Research Scientist, Baidu Silicon Valley AI Lab (SVAIL)
- 2013–2015: Data Scientist, Twitter
- 2010–2012: M.S. in Computer Science (Language Technologies), Carnegie Mellon University (advised by Roni Rosenfeld)
- 2006–2010: B.Tech in Computer Science, IIIT Hyderabad

## Leadership and Team Building

- Founding member of the FAIR Chemistry team at Meta and one of its technical leads — the team that produced the Open Catalyst Project, ODAC, OMC25, the UMA family of foundation models, and the fairchem library.
- Research Manager of the FAIR Speech team — led the team that built the first billion-parameter speech models, pioneered self-supervised and massively multilingual architectures, and deployed models to Facebook and Instagram serving billions of users.
- Led the fastMRI project at Meta AI — the collaboration with NYU Langone Health that produced the clinical standard for AI-accelerated MRI worldwide.

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
- Led FastCSP (lead author, 2025), a high-throughput molecular crystal structure prediction workflow powered entirely by the UMA MLIP. FastCSP accelerated organic CSP by approximately three orders of magnitude at high accuracy by replacing classical force fields and gold-standard DFT re-ranking with machine learning interatomic potentials — reducing CSP for a single system from weeks to hours on tens of GPUs.
- Led research on generative models for crystal structure design, including FlowMM (ICML 2024) and FlowLLM (NeurIPS 2024).

### Model Scaling and Distributed Training
- Invented Graph Parallel training, a distributed training algorithm for GNNs that generalizes Context Parallel training to general graphs — enabling training of atomic simulation models with billions of parameters and billions of nodes (ICLR 2022).
- First to scale speech recognition models to billions of parameters at Meta FAIR, building the earliest multi-billion-parameter speech models. Deployed to Facebook and Instagram serving billions of users, the models delivered significantly higher throughput and substantially lower latency than the previous production speech systems.
- Co-developed Deep Speech 2 at Baidu — one of the first systems to demonstrate that end-to-end deep learning scales predictably with data, compute, and model size (ICML 2016). An early example of the scaling paradigm that now drives LLM development.
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
- Led the fastMRI project at Meta AI, the collaboration with NYU Langone Health whose deep-learning reconstruction methods have become the clinical standard for AI-accelerated MRI worldwide. Co-first author on the fastMRI dataset release (Radiology: AI, 2020) and first author on the foundational reconstruction architectures — End-to-End Variational Networks (MICCAI 2020) and GrappaNet (CVPR 2020) — which are the foundation of the AI MRI reconstruction pipelines deployed in routine clinical practice today, validated prospectively in real-world clinical settings (Radiology, 2023; AJR, 2020).
- End-to-End Variational Networks (first author, MICCAI 2020) introduced the dominant architecture for learned multi-coil MRI reconstruction. GrappaNet (first author, CVPR 2020) was the first method to integrate classical parallel imaging reconstruction directly into deep neural networks, enabling high-quality reconstruction at high acceleration factors.
- Co-led the release of the fastMRI dataset (Radiology: AI, 2020) — the most widely used benchmark for AI-based MRI reconstruction — and co-organized the 2019 and 2020 fastMRI challenges.
- Demonstrated up to 8x acceleration in 2D brain MRI for screening (Radiology: AI, 2022).

### Self-Supervised Learning
- Developed Robust wav2vec 2.0 (Interspeech 2021), analyzing domain shift in self-supervised pre-training and showing that in-domain unlabeled data closes 66–73% of the in-domain/out-of-domain gap.
- Developed Wav2Vec-Aug (Interspeech 2022) for self-supervised pre-training in limited-data regimes.
- Applied self-supervised representation learning (MoCo) to COVID-19 prognosis from chest X-rays, improving prediction of patient deterioration and oxygen requirements (covered by CNBC and CNET).

### Speech Recognition (Baidu + Meta FAIR, 2015–2022)
- Co-created Deep Speech 2 at Baidu — one of the first large-scale end-to-end neural speech recognition systems, the first such model to achieve human-level recognition in both English and Mandarin (ICML 2016). Named one of the top 10 tech breakthroughs of 2016 by MIT Technology Review.
- Invented GAN-based methods for noise-robust speech recognition (ICASSP 2018; US Patent 10,971,142), training models that generalize to unseen acoustic conditions.
- Created Multilingual LibriSpeech (MLS) (Interspeech 2020), a large multilingual corpus of ~50K hours across 8 languages, widely used as the standard benchmark for multilingual speech.
- Built the first speech recognition models to transcribe over 50 languages with a single billion-parameter model (Massively Multilingual ASR, Interspeech 2020).
- Built and managed the FAIR Speech team, which trained and deployed the first billion-parameter speech models to Facebook and Instagram.

## Research Impact
- 65 publications, h-index of 42, ~15,000 citations on Google Scholar.
- Publications at top venues including NeurIPS, ICML, ICLR, CVPR, MICCAI, Interspeech, ICASSP, Nature Scientific Data, Radiology, IEEE TMI, ACS Catalysis, and ACS Central Science.
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


@main.route('/')
def home():
    return render_template('pages/home.html',
                         page={'title': None, 'permalink': '/'},
                         active_page='home')


@main.route('/publications/')
def publications():
    description = (
        '65 publications by Anuroop Sriram covering AI for Science, model scaling, '
        'diffusion and flow matching, MRI acceleration, and speech recognition. '
        'Includes work on UMA, Open Catalyst, FlowMM, FlowLLM, FastCSP, GrappaNet, '
        'End-to-End Variational Networks, Deep Speech 2, and Multilingual LibriSpeech.'
    )
    return render_template('pages/publications.html',
                         page={'title': 'Publications', 'permalink': '/publications/', 'description': description},
                         active_page='publications')


@main.route('/datasets/')
def datasets():
    description = (
        'Open scientific datasets created or co-created by Anuroop Sriram, including '
        'Open Catalyst (OC20, OC22), Open DAC (ODAC23, ODAC25), Open Molecular Crystals '
        '(OMC25), fastMRI, and Multilingual LibriSpeech (MLS).'
    )
    return render_template('pages/datasets.html',
                         page={'title': 'Datasets', 'permalink': '/datasets/', 'description': description},
                         active_page='datasets')


@main.route('/allnews/')
def allnews():
    description = (
        'Recent news and updates from Anuroop Sriram, including new papers, dataset releases, '
        'conference acceptances, and career milestones.'
    )
    return render_template('pages/allnews.html',
                         page={'title': 'News', 'permalink': '/allnews/', 'description': description},
                         active_page='news')


@main.route('/aboutwebsite/')
def aboutwebsite():
    description = (
        'About anuroopsriram.com — built with Flask and Frozen-Flask, deployed on GitHub Pages.'
    )
    return render_template('pages/aboutwebsite.html',
                         page={'title': 'About this website', 'permalink': '/aboutwebsite/', 'description': description},
                         active_page='about')


@main.route('/sitemap.xml')
def sitemap():
    pages = [
        {'loc': '/', 'priority': '1.0'},
        {'loc': '/publications/', 'priority': '0.8'},
        {'loc': '/datasets/', 'priority': '0.8'},
        {'loc': '/allnews/', 'priority': '0.5'},
        {'loc': '/aboutwebsite/', 'priority': '0.3'},
        {'loc': '/llms.txt', 'priority': '0.5'},
        {'loc': '/llms-full.txt', 'priority': '0.5'},
    ]
    site_url = current_app.config.get('SITE_URL', 'https://anuroopsriram.com')
    lastmod = datetime.utcnow().strftime('%Y-%m-%d')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        xml += f'  <url>\n'
        xml += f'    <loc>{site_url}{p["loc"]}</loc>\n'
        xml += f'    <lastmod>{lastmod}</lastmod>\n'
        xml += f'    <priority>{p["priority"]}</priority>\n'
        xml += f'  </url>\n'
    xml += '</urlset>'
    resp = make_response(xml)
    resp.headers['Content-Type'] = 'application/xml'
    return resp


@main.route('/robots.txt')
def robots():
    site_url = current_app.config.get('SITE_URL', 'https://anuroopsriram.com')
    txt = (
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        f'Sitemap: {site_url}/sitemap.xml\n'
        '\n'
        '# LLM-friendly summaries (for AI crawlers and tools):\n'
        f'# {site_url}/llms.txt\n'
        f'# {site_url}/llms-full.txt\n'
    )
    resp = make_response(txt)
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@main.route('/llms.txt')
def llms_txt():
    resp = make_response(LLMS_TXT_BODY)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


@main.route('/llms-full.txt')
def llms_full_txt():
    """Full-corpus LLM-friendly summary: bio + every publication, dataset, and news item."""
    txt = render_template('pages/llms_full.txt', bio=LLMS_TXT_BODY)
    resp = make_response(txt)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


