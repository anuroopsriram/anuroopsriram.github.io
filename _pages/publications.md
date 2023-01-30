---
title: "Publications"
layout: gridlay
sitemap: false
permalink: /publications/
---

# Publications

{% for myyear in site.data.years %}

{% assign yeartest = false %}
{% for publi in site.data.publist %}
  {% if publi.year == myyear.year %}
   {% assign yeartest = true %}
  {% endif %}
{% endfor %}

{% if site.group_pub_by_year == true %}
{% if yeartest == true %}
## {{ myyear.year }}
{% endif %}
{% endif %}

{% for publi in site.data.publist %}
{% if publi.year == myyear.year %}

<!-- {% assign bibtest = false %}
{% if publi.url %}
{% assign bibfile = "/papers/" | append:  publi.url  | append: ".txt" %}
{% for file in site.static_files %}
  {% if file.path contains bibfile %}
   {% assign bibtest = true %}
  {% endif %}
{% endfor %}
{% endif %} -->

<div class="well-sm">
<ul class="flex-container">
<li class="flex-item1">
  {% if publi.image %}
   <img src="{{ site.url }}{{ site.baseurl }}/images/pubpic/{{ publi.image }}" class="img-responsive" width="200%" style="float: left" />
  {% endif %}
</li>
<li class="flex-item2">
  <strong> {{ publi.title }}</strong> <br />
  <em><small>{{ publi.authors }} </small></em><br />
  <!-- {{ publi.display }} {% if publi.year %}({{publi.year}}){% endif %}<br/> -->
  <small><b>{{ publi.venue }}</b></small> 
  <!-- {% if publi.url %}<a href="{{ site.url }}{{ site.baseurl }}/papers/{{ publi.url }}.pdf" target="_blank"><button class="btn-pdf">PDF</button></a>{% endif %} -->
  <br/>

  {% if publi.doi %}<a href="http://dx.doi.org/{{ publi.doi }}" target="_blank"><button class="btn-common">DOI</button></a> {% endif %}
  {% if publi.arxiv %}<a href="https://arxiv.org/abs/{{ publi.arxiv }}" target="_blank"><button class="btn-common">ARXIV</button></a> {% endif %}
  {% if publi.link %}<a href="{{ publi.link }}" target="_blank"><button class="btn-common"> PAPER</button></a> {% endif %}
  {% if publi.pdf %}<a href="{{ site.url }}{{ site.baseurl }}/publications/pdfs/{{ publi.pdf }}" target="_blank"><button class="btn-bib">PDF</button></a> {% endif %}
  {% if publi.patent %}<a href="{{ publi.patent }}" target="_blank"><button class="btn-common">PATENT</button></a> {% endif %}
  <!-- {% if bibtest == true %} <a data-toggle="collapse" href="#{{publi.url}}2" class="btn-common" style="text-decoration:none; color:#ebebeb; hover:#ebebeb;" role="button" aria-expanded="false" aria-controls="{{publi.url}}2">BIB</a> {% endif %} -->
  {% if publi.abstract %} <a data-toggle="collapse" href="#{{publi.url}}_abs" class="btn-common" style="text-decoration:none; hover:#ebebeb;" role="button" aria-expanded="false" aria-controls="{{publi.url}}_abs">ABSTRACT</a>{% endif %}
  {% if publi.code %}<a href="{{ publi.code }}" target="_blank"><button class="btn-common">CODE</button></a> {% endif %}
  {% if publi.data %}<a href="{{ publi.data }}" target="_blank"><button class="btn-common">DATA</button></a> {% endif %}
  {% if publi.press %} <a data-toggle="collapse" href="#{{publi.url}}_press" class="btn-common" style="text-decoration:none; hover:#ebebeb;" role="button" aria-expanded="false" aria-controls="{{publi.url}}_press">MEDIA</a>{% endif %}

{% if publi.abstract %}
<br/>
<div class="collapse" id="{{publi.url}}_abs"><div class="well-abstract">
<small> <p align="justify"> {{publi.abstract | newline_to_br}} </p> </small>
</div></div>
{% endif %}

{% if publi.press %}
<small>
<br/>
<div class="collapse" id="{{publi.url}}_press">
<div class="well-abstract">
  <ul style="padding:-20px;list-style-position:ouside;">
  {% for article in publi.press %}
    <a href="{{article.link}}" target="_blank"> 
    <li style="list-style-image:url('{{site.url}}{{site.baseurl}}/images/logos/{{article.logo}}');"> 
      <!-- {{article.source}}:  -->
      "{{article.text}}"
      {% if article.author %} by {{article.author}}{% endif %}
    </li>
    </a>
  {% endfor %}
  </ul>
</div>
</div>
</small>
{% endif %}


{% if bibtest == true %}
<div class="collapse" id="{{publi.url}}2"><div class="well-bib">
<iframe src='{{site.url}}{{site.baseurl}}/papers/{{publi.url}}.txt' scrolling='yes' width="100%" height="210" frameborder='0'></iframe>
</div></div>
{% endif %}

</li>
</ul>

</div>
{% endif %}
{% endfor %}

{% endfor %}

