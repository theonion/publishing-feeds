# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Feed.url'
        db.alter_column(u'core_feed', 'url', self.gf('django.db.models.fields.URLField')(max_length=1024))

    def backwards(self, orm):

        # Changing field 'Feed.url'
        db.alter_column(u'core_feed', 'url', self.gf('django.db.models.fields.URLField')(max_length=200))

    models = {
        u'core.article': {
            'Meta': {'ordering': "['-publish_date']", 'object_name': 'Article'},
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['core.Edition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'kicker': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['core.Section']"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.edition': {
            'Meta': {'ordering': "['-published_date']", 'object_name': 'Edition'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'editions'", 'to': u"orm['core.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'core.feed': {
            'Meta': {'object_name': 'Feed'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024'})
        },
        u'core.publishingschedule': {
            'Meta': {'ordering': "['weekday', 'time']", 'object_name': 'PublishingSchedule'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule'", 'to': u"orm['core.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'weekday': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.section': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Section'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['core.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']