---
title: "Code"
layout: gridlay
sitemap: false
permalink: /code/
---

# Code

{% for code in site.data.codelist %}

  <div class="well-sm">
  <ul class="flex-container">
  <li class="flex-item1">
    {% if code.image %}
    <img src="{{ site.url }}{{ site.baseurl }}/images/codepic/{{ code.image }}" class="img-responsive" width="100%" style="float: left" />
    {% endif %}
    {% if code.video %}
    <video src="{{ site.url }}{{ site.baseurl }}/images/codepic/{{ code.video }}" autoplay="" class="hero-video w-100" width="200%" style="float: left" loop="" muted="" />
    {% endif %}
  </li>
  <li class="flex-item2">
    <strong> <a href="{{ code.link }}" target="_blank"> {{ code.title }} </a> </strong><br/>
    {{ code.description }}<br/>
  </li>
  </ul>
  </div>
{% endfor %}

