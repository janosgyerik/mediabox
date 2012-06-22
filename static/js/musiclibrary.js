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

    var AlbumSong = Backbone.Model.extend({
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

    var AppView = Backbone.View.extend({
        el: $('#musiclibrary'),
        initialize: function() {
            artists.bind('add', this.addOne, this);
            artists.bind('reset', this.addAll, this);
            artists.bind('all', this.render, this);

            this.main = $('#artists');

            artists.fetch();
        },
        render: function() {
            if (artists.length) {
                this.main.show();
            }
            else {
                this.main.hide();
            }
        },
        addOne: function(artist) {
            var view = new ArtistView({model: artist});
            this.$("#artist-list").append(view.render().el);
        },
        addAll: function() {
            artists.each(this.addOne);
        }
    });

    var app = new AppView;
});
