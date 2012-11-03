// setup mock objects and helpers
//
var options = {};
var obj;

function setUp() {
    create_filterpanel();
}

function create_filterpanel() {
    var html = $('<div id="filterpanel"/>');
    html.append($('.templates .filterpanel').clone());
    $('#demo').append(html);
    obj = $('#filterpanel').filterpanel(options);
}

QUnit.begin = setUp;

test('sanity tests', function() {
    ok(obj);
});

test('length', function() {
    ok(obj.filterpanel('length') > 0);
});

test('items', function() {
    ok(obj.filterpanel('items').length > 0);
});

test('selected items', function() {
    ok(obj.filterpanel('selectedItems').length == 0);
});

test('toggle items', function() {
    ok(obj.filterpanel('length') > 2);
    ok(obj.filterpanel('selectedItems').length == 0);
    obj.filterpanel('toggleItem', 0);
    ok(obj.filterpanel('selectedItems').length == 1);
    obj.filterpanel('toggleItem', 1);
    ok(obj.filterpanel('selectedItems').length == 2);
});

test('apply filter', function() {
    ok(obj.filterpanel('length') > 2);
    var text = obj.filterpanel('item', 0).substr(2).toUpperCase();
    obj.filterpanel('applyFilter', text);
    obj.filterpanel('clearFilter');
});


// eof
