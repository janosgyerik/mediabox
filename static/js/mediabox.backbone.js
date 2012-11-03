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
        title: 'TITLE',
        url: 'file.mp3',
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
    model: App.Media
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
        filters: {}
    },
    addFilter: function(name, value) {
        var filters = this.get('filters');
        if (filters.hasOwnProperty(name)) {
            filters[name].push(value);
        }
        else {
            filters[name] = [value];
        }
        this.trigger('change');
    },
    toString: function() {
        return JSON.stringify(this.get('filters'));
    },
    getFiltered: function(filterToSkip) {
        var list = this.get('list');
        var filters = this.get('filters');
        var filter = function(item) {
            for (var name in filters) {
                if (name == filterToSkip) {
                    continue;
                }
                if (!_.contains(filters[name], item.get(name))) {
                    return false;
                }
            }
            return true;
        };
        return list.filter(filter);
    }
});

App.ModelLogger = Backbone.View.extend({
    initialize: function() {
        var logger = function(what) {
            return function() {
                console.log(what, ':', this.model.toString());
            };
        };
        this.model.bind('change', logger('change'), this);
    }
});

App.FieldView = Backbone.View.extend({
    initialize: function(options) {
        this.model.bind('change', this.render, this);
        this.view = this.$('.list');
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.filterbox();
        this.selected = {};
    },
    render: function() {
        var html = this.$('.list');
        html.empty();
        var fieldName = this.fieldName();
        var pluck = function(item) { return item.get(fieldName); }
        var items = _.uniq(_.map(this.model.getFiltered(fieldName), pluck));
        _.each(items, function(item) {
            html.append($('<li/>').append(item));
        });
        for (name in this.selected) {
            this.$el.filterbox('select', name);
        }
        return this;
    },
    select: function(name) {
        this.selected[name] = true;
        this.$el.filterbox('select', name);
        this.model.addFilter(this.fieldName(), name);
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
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        var html = this.$('.list');
        _.each(this.model.getFiltered(), function(item) {
            var view = new App.MediaView({model: item});
            html.append(view.render().el);
        });
        var player = this.model.get('player');
        if (player) {
            player.addTracks('#medialist');
        }
        return this;
    }
});

function onDomReady() {
    // instances
    // TODO: put in setup.js
    App.mediaList = new App.MediaList();

    App.filter = new App.Filter({
        list: App.mediaList
    });

    App.artistsView = new App.ArtistsView({
        el: '#artists',
        model: App.filter
    });

    App.albumsView = new App.AlbumsView({
        el: '#albums',
        model: App.filter
    });

    App.mediaListView = new App.MediaListView({
        el: '#medialist',
        model: App.filter
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

    new App.ModelLogger({model: App.filter});

    App.albumsView.select('Roots');
    //App.filter.addFilter('artist', 'Metallica');
    //App.filter.addFilter('album', 'Master Of Puppets');

    // other initialization
    // force all views based on the filter to render
    App.filter.trigger('change');

    // debugging
    //App.keywordsView.create('sollicit');
}

function onPlayerReady() {
    console.log('onPlayerReady');
    var player = YAHOO.MediaPlayer;
    window.player = player;
    App.filter.set('player', player);
    var play = function() {
        console.log('play');
        player.play();
        player.play();
    };
    var onPlaylistUpdate = function() {
        console.log('onPlaylistUpdate');
        console.log(player);
        setTimeout(play, 1000);
    };
    player.onPlaylistUpdate.subscribe(onPlaylistUpdate);
};

$(function() {
    onDomReady();
    YAHOO.MediaPlayer.onAPIReady.subscribe(onPlayerReady);
});

// eof
