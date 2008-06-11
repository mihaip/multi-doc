$(main);

function main() {
  $("#search-form").submit(executeSearch);
  $("#q").keypress(executeSearchDelayed);
}

var searchTimeout_;

function executeSearchDelayed() {
  if (searchTimeout_) window.clearTimeout(searchTimeout_);
  
  searchTimeout_ = window.setTimeout(executeSearch, 400);
}

function executeSearch(e) {
  if (searchTimeout_) window.clearTimeout(searchTimeout_);
  searchTimeout_ = null;

  var query = $("#q").val();
  
  $.getJSON("/search?q=" + encodeURIComponent(query), null, renderResults);
}

function renderResults(results) {
  window.console.log(results);
}

