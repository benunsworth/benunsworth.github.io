---
layout: page
title: Tags
permalink: /tags/
---

{% assign sorted_tags = site.tags | sort %}

<div class="tags-cloud">
  {% for tag in sorted_tags %}
    {% assign tag_name = tag[0] %}
    {% assign tag_posts = tag[1] %}
    <a class="post-tag" href="#{{ tag_name | slugify }}">
      #{{ tag_name }} <span class="tag-count">({{ tag_posts.size }})</span>
    </a>
  {% endfor %}
</div>

{% for tag in sorted_tags %}
  {% assign tag_name = tag[0] %}
  {% assign tag_posts = tag[1] %}
  <div class="tag-section" id="{{ tag_name | slugify }}">
    <h2 class="tag-heading">#{{ tag_name }}</h2>
    <ul class="archive-list">
      {% for post in tag_posts %}
        <li class="archive-item">
          <a class="archive-title" href="{{ post.url | absolute_url }}">{{ post.title }}</a>
          <small class="archive-meta">
            {{ post.date | date_to_string }} &middot; {% include reading_time.html content=post.content %}
          </small>
        </li>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
