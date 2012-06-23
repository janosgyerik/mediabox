/*!
 * Music Library JavaScript Library v0.1
 * http://musiclibrary.titan2x.com/
 *
 * Copyright 2012, Janos Gyerik
 * http://musiclibrary.titan2x.com/LICENSE
 *
 * Date: Thu Jun 21 20:31:54 CEST 2012
 */

$(function() {
    var Genre = Backbone.Model.extend({
    });

    var Artist = Backbone.Model.extend({
    });

    var Album = Backbone.Model.extend({
    });

    var ArtistList = Backbone.Collection.extend({
        model: Artist,
        localStorage: new Store("artists-backbone"),
    });

    var artists = new ArtistList;

    var ArtistView = Backbone.View.extend({
        tagName: "li",
        template: _.template($('#artist-template').html()),
        events: {
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    var AlbumSong = Backbone.Model.extend({
    });

    var AlbumSongView = Backbone.View.extend({
        tagName: 'li',
        template: _.template($('#album-song-template').html()),
        events: {
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    var AlbumSongList = Backbone.Collection.extend({
        model: AlbumSong
    });

    var albumSongs = new AlbumSongList(albumSongs_raw);
    window.albumSongs = albumSongs;

    var searchResults = new AlbumSongList();
    window.searchResults = searchResults;

    var SearchBox = Backbone.View.extend({
        el: $('#searchbox'),
        events: {
            'keypress .search-text': 'applyFilterOnEnter'
        },
        initialize: function() {
            this.input = this.$('.search-text');

            searchResults.bind('add', this.addOne, this);
            searchResults.bind('reset', this.reset, this);
            searchResults.bind('all', this.render, this);
        },
        render: function() {
        },
        addOne: function(albumSong) {
            var view = new AlbumSongView({model: albumSong});
            this.$(".search-results").append(view.render().el);
        },
        reset: function() {
            this.$(".search-results").empty();
        },
        applyFilter: function(text) {
            text = text.toLowerCase();
            searchResults.reset();
            searchResults.add(
                    _.chain(albumSongs.filter(function() { return true }))
                    .filter(function(albumSong) {
                        return albumSong.get('relpath').toLowerCase().indexOf(text) > -1;
                    })
                    .sortBy(function(albumSong) {
                        return albumSong.get('relpath');
                    })
                    .value()
                    );
            YAHOO.MediaPlayer.addTracks($('.search-results'), 0, true);
        },
        applyFilterOnEnter: function(e) {
            if (e.keyCode != 13) return;
            if (!this.input.val()) return;
            this.applyFilter(this.input.val());
        }
    });

    var searchbox = new SearchBox;
    searchbox.input.focus();

    /*
    var AppView = Backbone.View.extend({
        initialize: function() {
            this.searchbox = new SearchBox();
        },
        render: function() {
            //this.searchbox.show();
        }
    });

    var app = new AppView;
    */
});
