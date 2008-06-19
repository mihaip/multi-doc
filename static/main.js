$(main);

function main() {
  $('#search-form').submit(executeSearch);
  $('#q').keypress(executeSearchDelayed);
  
  // If there's already a search filled in, re-run it (to handle refreshes)
  if ($('#q').val()) {
    executeSearch();
  }
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
    
    var groupHeaderNode = 
        $("<h1>" + group.name + "</h1>").appendTo(resultsNode);
    var groupNode = $("<ol></ol>").addClass("group").appendTo(resultsNode);

    var packageNode = null;
    var entriesNode = null;
    var packageName = null;
    
    for (var j = 0, entry; entry = entries[j]; j++) {
      if (entry["package"] != packageName) {
        packageName = entry["package"];

        packageNode = $("<li></li>").addClass("package").appendTo(groupNode);
        $('<h2>' + packageName + '</h2>').appendTo(packageNode);
        entriesNode = $('<ol></ol>').appendTo(packageNode);
        
      }
      
      $('<li><a href="#">' + entry.name + '</a></li>').addClass('entry').
          appendTo(entriesNode);
    }
  }
}

