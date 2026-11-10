---
layout: page
title: Archive
permalink: /archive/
---

<div class="search-box">
  <input type="search" id="search-input" class="search-input" placeholder="Search posts by title, tag, or keyword..." aria-label="Search posts" data-search-url="{{ '/search.json' | relative_url }}">
  <ul id="search-results" class="archive-list"></ul>
</div>

<div id="archive-content">
  {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
  {% for year in posts_by_year %}
    <h2>{{ year.name }}</h2>
    <ul class="archive-list">
      {% for post in year.items %}
        <li class="archive-item">
          <a class="archive-title" href="{{ post.url | absolute_url }}">{{ post.title }}</a>
          <small class="archive-meta">
            {{ post.date | date_to_string }} &middot; {% include reading_time.html content=post.content %}
          </small>
          {% include post_tags.html tags=post.tags %}
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
</div>
