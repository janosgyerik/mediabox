// setup mock objects and helpers
//
var options = {};
var obj;

function setUp() {
    create_filterbox();
}

function create_filterbox() {
    var html = $('<div id="filterbox"/>');
    html.append($('.templates .filterbox').clone());
    $('#demo').append(html);
    obj = $('#filterbox').filterbox(options);
}

QUnit.begin = setUp;

test('sanity tests', function() {
    ok(obj);
});

test('length', function() {
    ok(obj.filterbox('length') > 0);
});

test('items', function() {
    ok(obj.filterbox('items').length > 0);
});

test('selected items', function() {
    ok(obj.filterbox('selectedItems').length == 0);
});

test('toggle items', function() {
    ok(obj.filterbox('length') > 2);
    ok(obj.filterbox('selectedItems').length == 0);
    obj.filterbox('toggleItem', 0);
    ok(obj.filterbox('selectedItems').length == 1);
    obj.filterbox('toggleItem', 1);
    ok(obj.filterbox('selectedItems').length == 2);
});

test('apply filter', function() {
    ok(obj.filterbox('length') > 2);
    var text = obj.filterbox('item', 0).substr(2).toUpperCase();
    obj.filterbox('applyFilter', text);
    obj.filterbox('clearFilter');
});


// eof
