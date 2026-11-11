(function(document) {
  var toggle = document.querySelector('.sidebar-toggle');
  var sidebar = document.querySelector('#sidebar');
  var checkbox = document.querySelector('#sidebar-checkbox');

  if (checkbox && sidebar) {
    document.addEventListener('click', function(e) {
      var target = e.target;

      if(!checkbox.checked ||
         sidebar.contains(target) ||
         (target === checkbox || target === toggle)) return;

      checkbox.checked = false;
    }, false);
  }

  var searchInput = document.getElementById('search-input');
  var searchResults = document.getElementById('search-results');
  var archiveContent = document.getElementById('archive-content');
  var searchData = null;

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  function buildSearchBadgesHtml(post) {
    var rawType = (post.type || 'note').toLowerCase();
    var streamMap = {
      essay: 'Essay',
      weeknote: 'Weeknote',
      review: 'Review',
      note: 'Note'
    };
    var streamLabel = streamMap[rawType] || 'Note';
    var html = '<span class="post-meta-badges">' +
      '<span class="badge badge-stream badge-stream--' + escapeHtml(rawType) + '">' + escapeHtml(streamLabel) + '</span>';

    var rawMedia = (post.media || '').toLowerCase();
    var mediaMap = {
      book: 'Book',
      podcast: 'Podcast',
      tv: 'TV',
      film: 'Film',
      game: 'Game'
    };
    if (rawMedia && mediaMap[rawMedia]) {
      html += '<span class="badge badge-media badge-media--' + escapeHtml(rawMedia) + '">' + escapeHtml(mediaMap[rawMedia]) + '</span>';
    }

    if (post.rating) {
      html += '<span class="badge badge-media" role="img" aria-label="Rated ' + escapeHtml(String(post.rating)) + ' out of 5 stars">&#9733; ' + escapeHtml(String(post.rating)) + '/5</span>';
    }

    var rawStatus = (post.status || '').toLowerCase();
    var statusSvgs = {
      rough: '<svg class="status-glyph-svg" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" focusable="false"><circle cx="5" cy="5" r="4.1" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="2.2 1.8" stroke-linecap="round" /></svg>',
      'in-progress': '<svg class="status-glyph-svg" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" focusable="false"><circle cx="5" cy="5" r="4.1" fill="none" stroke="currentColor" stroke-width="1.3" /><path d="M 5,0.9 A 4.1,4.1 0 0,0 5,9.1 Z" fill="currentColor" /></svg>',
      settled: '<svg class="status-glyph-svg" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" focusable="false"><circle cx="5" cy="5" r="4.4" fill="currentColor" /></svg>'
    };
    var statusLabels = {
      rough: 'Rough',
      'in-progress': 'In progress',
      settled: 'Settled'
    };
    if (rawStatus && statusLabels[rawStatus]) {
      html += '<span class="badge badge-status badge-status-' + escapeHtml(rawStatus) + ' badge-status--' + escapeHtml(rawStatus) + '">' +
        statusSvgs[rawStatus] + '<span>' + escapeHtml(statusLabels[rawStatus]) + '</span></span>';
    }

    html += '</span>';
    return html;
  }

  function renderResults(query) {
    if (!searchResults || !archiveContent) return;
    var trimmed = query.trim().toLowerCase();

    if (!trimmed) {
      searchResults.innerHTML = '';
      archiveContent.style.display = '';
      return;
    }

    archiveContent.style.display = 'none';
    if (!searchData) return;

    var matches = searchData.filter(function(post) {
      var inTitle = post.title && post.title.toLowerCase().indexOf(trimmed) !== -1;
      var inTags = post.tags && post.tags.join(' ').toLowerCase().indexOf(trimmed) !== -1;
      var inSummary = post.summary && post.summary.toLowerCase().indexOf(trimmed) !== -1;
      var inType = post.type && post.type.toLowerCase().indexOf(trimmed) !== -1;
      var inStatus = post.status && post.status.toLowerCase().indexOf(trimmed) !== -1;
      var inMedia = post.media && post.media.toLowerCase().indexOf(trimmed) !== -1;
      var inContent = post.content && post.content.toLowerCase().indexOf(trimmed) !== -1;
      return inTitle || inTags || inSummary || inType || inStatus || inMedia || inContent;
    });

    if (matches.length === 0) {
      searchResults.innerHTML = '<li class="archive-item">No matching posts found.</li>';
      return;
    }

    searchResults.innerHTML = matches.map(function(post) {
      var snippet = '';
      if (post.content && post.content.toLowerCase().indexOf(trimmed) !== -1) {
        var idx = post.content.toLowerCase().indexOf(trimmed);
        var start = idx > 40 ? idx - 40 : 0;
        var rawSnippet = post.content.slice(start, start + 160);
        snippet = '<div class="search-snippet">' +
          (start > 0 ? '&hellip;' : '') +
          escapeHtml(rawSnippet) +
          (start + 160 < post.content.length ? '&hellip;' : '') +
          '</div>';
      } else if (post.summary) {
        snippet = '<div class="search-snippet">' + escapeHtml(post.summary) + '</div>';
      }

      var updatedMeta = post.updated ? ' &middot; Tended ' + escapeHtml(post.updated) : '';

      return '<li class="archive-item">' +
        '<div class="archive-item-header">' +
          '<a class="archive-title" href="' + escapeHtml(post.url) + '">' + escapeHtml(post.title) + '</a>' +
          buildSearchBadgesHtml(post) +
        '</div>' +
        '<small class="archive-meta">Planted ' + escapeHtml(post.date) + updatedMeta + ' &middot; ' + escapeHtml(post.reading_time) + '</small>' +
        snippet +
      '</li>';
    }).join('');
  }

  if (searchInput) {
    var searchUrl = searchInput.getAttribute('data-search-url') || '/search.json';
    var loadSearchData = function() {
      if (searchData) return;
      fetch(searchUrl)
        .then(function(res) { return res.json(); })
        .then(function(data) {
          searchData = data;
          if (searchInput.value) renderResults(searchInput.value);
        })
        .catch(function() {});
    };

    searchInput.addEventListener('focus', loadSearchData);
    searchInput.addEventListener('input', function(e) {
      loadSearchData();
      renderResults(e.target.value);
    });
  }

  var filterButtons = document.querySelectorAll('.filter-pill[data-filter-group]');
  var gardenCards = document.querySelectorAll('#garden-grid .garden-card');
  var gardenCount = document.getElementById('garden-count');
  var gardenEmptyState = document.getElementById('garden-empty-state');
  var gardenResetBtn = document.getElementById('garden-reset-filters');

  if (filterButtons.length > 0 && gardenCards.length > 0) {
    var totalEntries = gardenCards.length;
    var activeFilters = {
      type: 'all',
      status: 'all',
      media: 'all'
    };

    var syncFilterPills = function() {
      for (var i = 0; i < filterButtons.length; i++) {
        var btn = filterButtons[i];
        var group = btn.getAttribute('data-filter-group');
        var val = btn.getAttribute('data-filter-value');
        var isActive = (activeFilters[group] === val);
        if (isActive) {
          btn.classList.add('active');
          btn.setAttribute('aria-pressed', 'true');
        } else {
          btn.classList.remove('active');
          btn.setAttribute('aria-pressed', 'false');
        }
      }
    };

    var applyGardenFilters = function() {
      var visibleCount = 0;
      for (var i = 0; i < gardenCards.length; i++) {
        var card = gardenCards[i];
        var cardType = card.getAttribute('data-type') || '';
        var cardStatus = card.getAttribute('data-status') || '';
        var cardMedia = card.getAttribute('data-media') || '';

        var matchesType = (activeFilters.type === 'all') || (cardType === activeFilters.type);
        var matchesStatus = (activeFilters.status === 'all') || (cardStatus === activeFilters.status);
        var matchesMedia = (activeFilters.media === 'all') || (cardMedia === activeFilters.media);

        if (matchesType && matchesStatus && matchesMedia) {
          card.hidden = false;
          visibleCount++;
        } else {
          card.hidden = true;
        }
      }

      if (gardenCount) {
        gardenCount.textContent = 'Showing ' + visibleCount + ' of ' + totalEntries + (totalEntries === 1 ? ' entry' : ' entries');
      }

      if (gardenEmptyState) {
        gardenEmptyState.hidden = (visibleCount > 0);
      }
    };

    for (var i = 0; i < filterButtons.length; i++) {
      filterButtons[i].addEventListener('click', function(e) {
        var btn = e.currentTarget;
        var group = btn.getAttribute('data-filter-group');
        var val = btn.getAttribute('data-filter-value');
        if (!group || !val) return;
        activeFilters[group] = val;
        syncFilterPills();
        applyGardenFilters();
      });
    }

    if (gardenResetBtn) {
      gardenResetBtn.addEventListener('click', function() {
        activeFilters.type = 'all';
        activeFilters.status = 'all';
        activeFilters.media = 'all';
        syncFilterPills();
        applyGardenFilters();
      });
    }
  }
})(document);
