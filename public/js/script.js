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
      var inContent = post.content && post.content.toLowerCase().indexOf(trimmed) !== -1;
      return inTitle || inTags || inContent;
    });

    if (matches.length === 0) {
      searchResults.innerHTML = '<li class="archive-item">No matching posts found.</li>';
      return;
    }

    searchResults.innerHTML = matches.map(function(post) {
      var snippet = '';
      if (post.content) {
        var idx = post.content.toLowerCase().indexOf(trimmed);
        var start = idx > 40 ? idx - 40 : 0;
        var rawSnippet = post.content.slice(start, start + 160);
        snippet = '<div class="search-snippet">' +
          (start > 0 ? '&hellip;' : '') +
          escapeHtml(rawSnippet) +
          (start + 160 < post.content.length ? '&hellip;' : '') +
          '</div>';
      }
      return '<li class="archive-item">' +
        '<a class="archive-title" href="' + escapeHtml(post.url) + '">' + escapeHtml(post.title) + '</a>' +
        '<small class="archive-meta">' + escapeHtml(post.date) + ' &middot; ' + escapeHtml(post.reading_time) + '</small>' +
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
})(document);
