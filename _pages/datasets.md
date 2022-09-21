---
title: "Datasets"
layout: gridlay
sitemap: false
permalink: /datasets/
---

# Datasets

{% for dataset in site.data.datalist %}

  <div class="well-sm">
  <ul class="flex-container">
  <li class="flex-item1">
    {% if dataset.image %}
    <img src="{{ site.url }}{{ site.baseurl }}/images/datapic/{{ dataset.image }}" class="img-responsive" width="100%" style="float: left" />
    {% endif %}
    {% if dataset.video %}
    <video src="{{ site.url }}{{ site.baseurl }}/images/datapic/{{ dataset.video }}" autoplay="" class="hero-video w-100" width="200%" style="float: left" loop="" muted="" />
    {% endif %}
  </li>
  <li class="flex-item2">
    <strong> {{ dataset.title }} </strong><br/>
    {{ dataset.description }}<br/>
    {% if dataset.project_url %}<a href="{{ dataset.project_url }}" target="_blank"><button class="btn-arxiv">PROJECT</button></a> {% endif %}
    {% if dataset.data_url %}<a href="{{ dataset.data_url }}" target="_blank"><button class="btn-data">DATA</button></a> {% endif %}
    {% if dataset.code_url %}<a href="{{ dataset.code_url }}" target="_blank"><button class="btn-code">CODE</button></a> {% endif %}
  </li>
  </ul>
  </div>
{% endfor %}

