/*!
 * PROEJCT backbone JavaScript Library v0.1
 * http://.../
 *
 * Copyright 2012, NAME
 * http://.../license
 *
 * Date: Fri Nov  2 19:02:58 CET 2012
 */


// the basic namespace
// TODO: put in app.js
window.App = {};

_.templateSettings = { interpolate: /\{\{(.+?)\}\}/g };

// classes
// TODO: put in app/*.js


App.Model = Backbone.Model.extend({
    defaults: {
    },
    initialize: function() {
        this.on('change:original', this.onOriginalUpdated, this);
        this.on('change:keywords', this.onKeywordsUpdated, this);
    },
    updateWords: function() {
        var words = {};
        _.each(this.get('original').split(/\W+/), function(word) {
            word = word.toLowerCase();
            words[word] = (words[word] || 0) + 1;
        });
        this.set({words: words});
    },
    updateHighlighted: function() {
        var highlighted = this.escape('original');
        var cnt = 1;
        _.each(this.get('keywords'), function(keyword) {
            var pattern = '\\b' + keyword;
            var cname = 'hlt' + cnt++;
            highlighted = highlighted.replace(new RegExp(pattern, 'gi'), '<span class="' + cname + '">' + keyword + '</span>');
        });
        this.set({highlighted: highlighted});
    },
    onOriginalUpdated: function() {
        this.updateWords();
        this.updateHighlighted();
    },
    onKeywordsUpdated: function() {
        this.updateHighlighted();
    },
    getCount: function(word) {
        var pattern = '\\b' + word;
        var matches = this.get('original').match(new RegExp(pattern, 'gi'));
        return matches ? matches.length : 0;
    }
});

App.Keyword = Backbone.Model.extend({
    defaults: {
        keyword: 'empty keyword...',
        count: 0,
        index: 1
    },
    clear: function() {
        this.destroy();
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
    edit: function() {
        this.$el.addClass('editing');
        this.input.focus();
    },
    close: function() {
        var value = this.input.val();
        if (!value) this.clear();
        this.model.set({keyword: value});
        this.$el.removeClass('editing');
    },
    updateOnEnter: function(e) {
        if (e.keyCode == 13) this.close();
    },
    clear: function() {
        this.model.clear();
    }
});

App.KeywordList = Backbone.Collection.extend({
    model: App.Keyword,
    localStorage: new Store('highlighter-backbone'),
    initialize: function() {
        this.on('add', this.onChange, this);
        this.on('remove', this.onChange, this);
        this.on('reset', this.onChange, this);
    },
    onChange: function() {
        var keywords = this.pluck('keyword');
        App.model.set({keywords: keywords});
        App.highlightedTab.activate();
    }
});

App.KeywordListView = Backbone.View.extend({
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

function onDomReady() {
    // instances
    // TODO: put in setup.js
    //App.model = new App.Model();

    //App.keywordListView = new App.KeywordListView({
        //model: App.model,
        //list: App.keywordList
    //});

    // other initialization
    //App.keywordListView.input.focus();
    //App.model.set({original: App.originalTab.text.text()});

    // debugging
    //App.highlightedTab.activate();
    //App.keywordListView.create('lorem');
    //App.keywordListView.create('pharet');
    //App.keywordListView.create('sollicit');
}

$(function() {
    onDomReady();
});

// eof
