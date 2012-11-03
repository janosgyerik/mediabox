/*!
 * MediaBox backbone JavaScript Library v0.1
 * http://.../
 *
 * Copyright 2012, NAME
 * http://.../license
 *
 * Date: Fri Nov  2 19:32:58 CET 2012
 */


// the basic namespace
// TODO: put in app.js
window.App = {};

//_.templateSettings = { interpolate: /\{\{(.+?)\}\}/g };

// classes
// TODO: put in app/*.js


App.Media = Backbone.Model.extend({
    defaults: {
        genre: 'GENRE',
        artist: 'ARTIST',
        album: 'ALBUM',
        title: 'TITLE'
    }
});

App.MediaList = Backbone.Collection.extend({
    model: App.Media,
    filtered: function() {
        var filter = function(item) { return true; };
        return this.filter(filter);
    }
});

App.KeywordView = Backbone.View.extend({
    tagName: 'tr',
    //template: _.template($('#keyword-template').html()),
    events: {
        'dblclick .view': 'edit',
        'click a.destroy': 'clear',
        'keypress .edit': 'updateOnEnter',
        'blur .edit': 'close'
    },
    initialize: function() {
        this.model.bind('change', this.render, this);
        this.model.bind('destroy', this.remove, this);
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        this.input = this.$('.edit');
        return this;
    },
    updateOnEnter: function(e) {
        if (e.keyCode == 13) this.close();
    },
    clear: function() {
        this.model.clear();
    }
});

App.Filter = Backbone.Model.extend({
    defaults: {
        genre: [],
        artist: [],
        album: []
    }
});

App.KeywordsView = Backbone.View.extend({
    el: '#keywords',
    events: {
        'keypress .keyword': 'createOnEnter',
        'click th a.destroy': 'clear'
    },
    initialize: function(options) {
        this.keywords = options.list;
        this.input = this.$('.keyword');
        this.keywords.bind('add', this.add, this);
        this.keywords.bind('reset', this.reset, this);
        this.keywords.fetch();
        if (this.keywords.length) {
            this.keywords.each(this.add);
        }
        else {
            this.create('lorem');
            this.create('ipsum');
            this.create('dolor');
        }
    },
    add: function(keyword) {
        var view = new App.KeywordView({model: keyword});
        this.$('#keyword-list').append(view.render().el);
    },
    reset: function() {
        this.$('#keyword-list').empty();
    },
    createOnEnter: function(e) {
        if (e.keyCode != 13) return;
        if (!this.input.val()) return;
        var keyword = this.input.val();
        this.create(keyword);
        this.input.val('');
    },
    create: function(keyword) {
        var index = this.keywords.length + 1;
        this.keywords.create({keyword: keyword, index: index});
    },
    clear: function() {
        // todo: isn't there a better way?
        var i = 0;
        var maxiter = 10;
        while (true) {
            this.keywords.invoke('destroy');
            if (!this.keywords.length || ++i > maxiter) break;
        }
    }
});

App.ArtistsView = Backbone.View.extend({
    el: '#artists',
    initialize: function(options) {
        this.mediaList = options.list;
        this.model.bind('change', this.render, this);
        this.view = this.$('.list');
    },
    render: function() {
        // todo: get filtered list from model
        // param: field to pluck = 'artist'
        // todo: generalize this in a parent class
        // todo: update dom with results, do not rewrite
        // or, merge results with the model that tracks Artist selection state
        this.view.empty();
        var html = $('<ul/>');
        var items;
        items = this.mediaList.toArray();
        // matches all objects that are Metallica
        items = this.mediaList.where({artist: 'Metallica'});
        // ... AND Sanitarium
        items = this.mediaList.where({artist: 'Metallica', title: 'Sanitarium'});
        _.each(items, function(item) {
            html.append($('<li/>').append(item.get('title')));
        });
        this.$el.append(html);
        html = $('<ol/>');
        items = _.uniq(this.mediaList.pluck('artist'));
        _.each(items, function(item) {
            html.append($('<li/>').append(item));
        });
        this.$el.append(html);
    }
});

App.AlbumsView = Backbone.View.extend({
    el: '#albums',
    template: _.template($('#albums-template').html()),
    initialize: function(options) {
        this.model.bind('change', this.render, this);
        this.mediaList = options.list;
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        this.view = this.$('.list');
        var html = $('<ul/>');
        _.each(this.mediaList.filtered(), function(item) {
            html.append($('<li/>').append(item.get('album')));
        });
        this.$el.append(html);
        return this;
    }
});

App.MediaListView = Backbone.View.extend({
    el: '#medialist',
    template: _.template($('#medialist-template').html()),
    initialize: function(options) {
        this.model.bind('change', this.render, this);
        this.mediaList = options.list;
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        this.view = this.$('.list');
        var html = $('<ul/>');
        _.each(this.mediaList.filtered(), function(item) {
            html.append($('<li/>').append(item.get('title')));
        });
        this.$el.append(html);
        return this;
    }
});

function onDomReady() {
    // instances
    // TODO: put in setup.js
    App.filter = new App.Filter();

    App.mediaList = new App.MediaList();

    App.artistsView = new App.ArtistsView({
        model: App.filter,
        list: App.mediaList
    });

    App.albumsView = new App.AlbumsView({
        model: App.filter,
        list: App.mediaList
    });

    App.mediaListView = new App.MediaListView({
        model: App.filter,
        list: App.mediaList
    });

    App.mediaList.add({title: 'Sanitarium', artist: 'Metallica', album: 'Master Of Puppets'});
    App.mediaList.add({title: 'Enter Sandman', artist: 'Metallica', album: 'Black Album'});
    App.mediaList.add({title: 'Biotech', artist: 'Sepultura', album: 'Chaos A.D.'});
    App.filter.trigger('change');

    // other initialization
    //App.keywordsView.input.focus();
    //App.model.set({original: App.originalTab.text.text()});

    // debugging
    //App.keywordsView.create('sollicit');
}

$(function() {
    onDomReady();
});

// eof



////MediaCollection
//-> media objects // constant

////FilteredMediaCollection
//-> sub-set of objects as matched by filter
// affect by filter

////UniqueProjection
////-> the unique values of a field=artist,album,...
// shows values based on FilteredMediaCollection
// also affected by local filter
// local filter does not trigger model change
// only clicks trigger model change
// hide/unhide, do NOT recreate dom

////filtered media list
// also a projection
// items not clickable, not trigger filter
// local filter allowed

////qunit
// select x -> check result list


// eof
