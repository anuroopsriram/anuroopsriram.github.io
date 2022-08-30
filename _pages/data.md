---
title: "Datasets"
layout: gridlay
sitemap: false
permalink: /data/
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
    <strong> <a href="{{ dataset.link }}" target="_blank"> {{ dataset.title }} </a> </strong><br/>
    {{ dataset.description }}<br/>
  </li>
  </ul>
  </div>
{% endfor %}

