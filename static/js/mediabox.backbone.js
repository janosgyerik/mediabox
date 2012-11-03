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

App.MediaView = Backbone.View.extend({
    tagName: 'li',
    template: _.template($('#media-template').html()),
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
});

App.MediaList = Backbone.Collection.extend({
    model: App.Media,
    filtered: function() {
        var filter = function(item) { return true; };
        return this.filter(filter);
    }
});

/*
App.KeywordView = Backbone.View.extend({
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
    updateOnEnter: function(e) {
        if (e.keyCode == 13) this.close();
    },
    clear: function() {
        this.model.clear();
    }
});
*/

App.Filter = Backbone.Model.extend({
    defaults: {
        genre: [],
        artist: [],
        album: []
    }
});

App.FieldView = Backbone.View.extend({
    initialize: function(options) {
        this.mediaList = options.list;
        this.model.bind('change', this.render, this);
        this.view = this.$('.list');
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        var html = this.$('.list');
        var fieldName = this.fieldName();
        var pluck = function(item) { return item.get(fieldName); }
        var items = _.uniq(_.map(this.mediaList.filtered(), pluck));
        _.each(items, function(item) {
            html.append($('<li/>').append(item));
        });
        return this;
    }
});

App.ArtistsView = App.FieldView.extend({
    template: _.template($('#artists-template').html()),
    fieldName: function() { return 'artist'; }
});

App.AlbumsView = App.FieldView.extend({
    template: _.template($('#albums-template').html()),
    fieldName: function() { return 'album'; }
});

App.MediaListView = Backbone.View.extend({
    template: _.template($('#medialist-template').html()),
    initialize: function(options) {
        this.model.bind('change', this.render, this);
        this.mediaList = options.list;
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        var html = this.$('.list');
        _.each(this.mediaList.filtered(), function(item) {
            var view = new App.MediaView({model: item});
            html.append(view.render().el);
        });
        return this;
    }
});

function onDomReady() {
    // instances
    // TODO: put in setup.js
    App.filter = new App.Filter();

    App.mediaList = new App.MediaList();

    App.artistsView = new App.ArtistsView({
        el: '#artists',
        model: App.filter,
        list: App.mediaList
    });

    App.albumsView = new App.AlbumsView({
        el: '#albums',
        model: App.filter,
        list: App.mediaList
    });

    App.mediaListView = new App.MediaListView({
        el: '#medialist',
        model: App.filter,
        list: App.mediaList
    });

    App.mediaList.add({title: 'Battery', artist: 'Metallica', album: 'Master Of Puppets'});
    App.mediaList.add({title: 'Sanitarium', artist: 'Metallica', album: 'Master Of Puppets'});
    App.mediaList.add({title: 'Enter Sandman', artist: 'Metallica', album: 'Metallica'});
    App.mediaList.add({title: 'Wherever I May Roam', artist: 'Metallica', album: 'Metallica'});
    App.mediaList.add({title: 'Propaganda', artist: 'Sepultura', album: 'Chaos A.D.'});
    App.mediaList.add({title: 'Biotech Is Godzilla', artist: 'Sepultura', album: 'Chaos A.D.'});
    App.mediaList.add({title: 'Nomad', artist: 'Sepultura', album: 'Chaos A.D.'});
    App.mediaList.add({title: 'Roots', artist: 'Sepultura', album: 'Roots'});
    App.mediaList.add({title: 'Spit', artist: 'Sepultura', album: 'Roots'});
    App.mediaList.add({title: 'Endangered Species', artist: 'Sepultura', album: 'Roots'});
    App.mediaList.add({title: 'Moses', artist: 'Soulfly', album: 'Prophecy'});
    App.mediaList.add({title: 'Porrada', artist: 'Soulfly', album: 'Prophecy'});
    App.mediaList.add({title: 'Get Out', artist: 'Faith No More', album: 'King For A Day'});
    App.mediaList.add({title: 'The Gentle Art Of Making Enemies', artist: 'Faith No More', album: 'King For A Day'});
    App.mediaList.add({title: 'Digging The Grave', artist: 'Faith No More', album: 'King For A Day'});

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
