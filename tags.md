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
  {% assign tag_slug = tag_name | slugify %}
  <div class="tag-section" id="{{ tag_slug }}">
    <h2 class="tag-heading">#{{ tag_name }}</h2>
    <ul class="archive-list">
      {% for post in tag_posts %}
        {% assign badge_prefix = tag_slug | append: "-" | append: post.url %}
        <li class="archive-item">
          <div class="archive-item-header">
            <a class="archive-title" href="{{ post.url | absolute_url }}">{{ post.title }}</a>
            {% include post_meta_badges.html post=post id_prefix=badge_prefix %}
          </div>
          <small class="archive-meta">
            <span>Planted {{ post.date | date_to_string }}</span>
            {%- if post.updated and post.updated != "" -%}
            <span>&middot; Tended {{ post.updated | date_to_string }}</span>
            {%- endif -%}
            <span>&middot; {% include reading_time.html content=post.content %}</span>
          </small>
        </li>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
