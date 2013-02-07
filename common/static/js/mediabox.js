/*!
 * MediaBox JavaScript Library v0.1
 * http://mediabox.titan2x.com/
 *
 * Copyright 2012, Janos Gyerik
 * http://mediabox.titan2x.com/LICENSE
 *
 * Date: Thu Jun 21 20:31:54 CEST 2012
 */

window.App = {};

// app constants
App.MAX_RECENT_FOLDERS = 15;

App.Folder = Backbone.Model.extend({
    defaults: {
        name: null,
        href: null
    }
});

App.FolderView = Backbone.View.extend({
    tagName: 'li',
    template: _.template($('#folder-template').html()),
    events: {
        'click a.destroy': 'clear'
    },
    initialize: function() {
        this.model.bind('destroy', this.remove, this);
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    clear: function() {
        this.model.clear();
    }
});

App.RecentFolderList = Backbone.Collection.extend({
    model: App.Folder,
    localStorage: new Store('mediabox-recent-folders'),
    addCustom: function(obj) {
        var filter = function(item) {
            return item.get('name') == obj.name;
        };
        var remove = function(item) {
            item.destroy();
        };
        _.each(this.filter(filter), remove);
        this.create(obj);
        var itemsToSlice = this.length - App.MAX_RECENT_FOLDERS;
        if (itemsToSlice > 0) {
            _.each(this.toArray().slice(itemsToSlice), remove);
        }
        this.trigger('updated');
    }
});

App.RecentFolderListView = Backbone.View.extend({
    el: '#recent-folders',
    initialize: function(options) {
        this.list = options.list;
        this.list.bind('reset', this.render, this);
        this.list.bind('updated', this.render, this);
        this.list.fetch();
    },
    render: function() {
        this.$('.list').empty();
        this.list.each(this.add);
        if (this.list.length) {
            this.$el.removeClass('gone');
        }
        else {
            this.$el.addClass('gone');
        }
    },
    add: function(folder) {
        var view = new App.FolderView({model: folder});
        this.$('.list').prepend(view.render().el);
    }
});

function onDomReady() {
    App.recentFolderList = new App.RecentFolderList();
    App.recentFolderListView = new App.RecentFolderListView({
        list: App.recentFolderList
    });
    var foldername = $('#foldername').text().trim();
    App.recentFolderList.addCustom({name: foldername, href: document.location.href});
}

$(function() {
    onDomReady();
});
