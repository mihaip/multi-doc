$(main);

function main() {
  // Attach event handlers
  $('#search-form').submit(executeSearch);
  $('#q').keypress(executeSearchDelayed);
  $(window).resize(updateResultsHeight);
  
  updateResultsHeight();
  
  // If there's already a search filled in, re-run it (to handle refreshes)
  if ($('#q').val()) {
    executeSearch();
  }
  
  // Similarly, if there's a search param in the URL, use that (to allow
  // the site to be used a keyword bookmark)
  if ($.query.get('q')) {
    $('#q').val($.query.get('q'));
    executeSearch();
  }
}

function updateResultsHeight() {
  var windowHeight = $(window).height();
  
  $('#results').css({
    height: (windowHeight - $('#results')[0].offsetTop) + 'px'
  });
}

var searchTimeout_;

function executeSearchDelayed() {
  if (searchTimeout_) window.clearTimeout(searchTimeout_);
  
  searchTimeout_ = window.setTimeout(executeSearch, 400);
}

function executeSearch(e) {
  if (searchTimeout_) window.clearTimeout(searchTimeout_);
  searchTimeout_ = null;

  var query = $('#q').val();
  
  $.getJSON('/search?q=' + encodeURIComponent(query), null, renderResults);
}

function renderResults(results) {
  var resultsNode = $('#results');
  
  resultsNode.empty()
  
  for (var i = 0, groupResults; groupResults = results[i]; i++) {
    var group = groupResults.group;
    var entries = groupResults.entries;
    var doctype = DOCTYPES[group.doctype];
    
    var groupHeaderNode = 
        $('<h1>' + group.name + '</h1>').appendTo(resultsNode);
    var groupNode = $('<ol></ol>').addClass('group').appendTo(resultsNode);

    var packageNode = null;
    var entriesNode = null;
    var packageName = null;
    
    for (var j = 0, entry; entry = entries[j]; j++) {
      if (entry['package'] != packageName) {
        packageName = entry['package'];

        packageNode = $('<li></li>').addClass('package').appendTo(groupNode);
        $('<h2>' + packageName + '</h2>').appendTo(packageNode);
        entriesNode = $('<ol></ol>').appendTo(packageNode);
        
      }
      
      var entryNode = $('<li></li>')
          .addClass('entry')
          .addClass(group.doctype + '-' + entry.type)
          .appendTo(entriesNode);
      var entryLinkNode = $('<a>' + entry.name + '</a>')
          .appendTo(entryNode)
          .attr('target', 'entry-frame')
          .attr('href', doctype.getEntryUrl(group, entry));
    }
  }
}

function JavadocDoctype() {}

JavadocDoctype.prototype.getEntryUrl = function(group, entry) {
  var rootUrl = group.rootUrl;
  var packagePath = entry['package'].replace(/\./g, '/');
  
  return rootUrl + packagePath + '/' + entry.name + '.html';
}

function MdcDoctype() {}

MdcDoctype.prototype.getEntryUrl = function(group, entry) {
  var rootUrl = group.rootUrl;
  var pageUrl;
  
  if (entry['package'] == 'CSS') {
    pageUrl = 'CSS:' + entry.name;
  }
  
  return rootUrl + pageUrl;
}

function W3cDoctype() {}

W3cDoctype.prototype.getEntryUrl = function(group, entry) {
  var rootUrl = group.rootUrl;
  var pageUrl;
  
  if (entry['package'] == 'HTML') {
    pageUrl = '/TR/html401/index/' + entry.type + 
        '#edef-' + entry.name.toUpperCase();
  }
  
  return rootUrl + pageUrl;
}

var DOCTYPES = {
  'javadoc': new JavadocDoctype(),
  'mdc': new MdcDoctype(),
  'w3c': new W3cDoctype()
};