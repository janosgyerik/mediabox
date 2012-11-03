/*!
 * jQuery filterbox Plugin v1.0
 *
 * Filter panel widget.
 *
 * ...
 *
 * How it works:
 * ...
 *
 * Date: Sat Nov  3 07:37:03 CET 2012
 * Requires: jQuery v1.3+, taffy 2.4+
 *
 * Copyright 2012, Janos Gyerik
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
*/

(function($){  
    var defaults = {  
    }; 

    var obj;
    var options;

    function _init(options_) {
        obj = this;
        options = $.extend(defaults, options_);
        return this;
    }

    function _length() {
        return obj.find('li').length;
    }

    function _items() {
        return obj.find('li').map(function() { return $(this).text(); });
    }

    function _item(num) {
        return _items()[num];
    }

    function _selectedItems() {
        return obj.find('li.selected').map(function() { return $(this).text(); });
    }

    function _visibleItems() {
        return obj.find('li:visible').map(function() { return $(this).text(); });
    }

    function _toggleItem(num) {
        return obj.find('li').eq(num).toggleClass('selected');
    }

    function _applyFilter(text) {
        text = text ? text.toLowerCase() : '';
        obj.find('li').each(function() {
            if ($(this).text().toLowerCase().indexOf(text) > -1) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        })
        return this;
    }

    function _clearFilter() {
        obj.find('.filter').val('');
        _applyFilter('');
        return this;
    }

    function _clear() {
        obj.find('.filter').val('');
        obj.find('li').remove();
        return this;
    }

    var methods = {
        init: _init,

        length: _length,
        item: _item,
        items: _items,
        selectedItems: _selectedItems,
        visibleItems: _visibleItems,
        toggleItem: _toggleItem,
        applyFilter: _applyFilter,
        clearFilter: _clearFilter,
        clear: _clear,

        destroy: _destroy
    };

    function _destroy() {
        return this.each(function() {
            $(window).unbind('.filterbox');
            //var $this = $(this), data = $this.data('filterbox');
            ////data.filterbox.remove();
            ////$this.removeData('filterbox');
        });
    }

    $.fn.filterbox = function(method) {  
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        }
        else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        }
        else {
            $.error('Method ' + method + ' does not exist on jQuery.filterbox');
        }
    };  
})(jQuery);
