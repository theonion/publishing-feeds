# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table(u'core_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'core', ['Feed'])

        # Adding model 'PublishingSchedule'
        db.create_table(u'core_publishingschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedule', to=orm['core.Feed'])),
            ('weekday', self.gf('django.db.models.fields.IntegerField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'core', ['PublishingSchedule'])

        # Adding model 'Section'
        db.create_table(u'core_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['core.Feed'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Section'])

        # Adding model 'Edition'
        db.create_table(u'core_edition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='editions', to=orm['core.Feed'])),
        ))
        db.send_create_signal(u'core', ['Edition'])

        # Adding model 'Article'
        db.create_table(u'core_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['core.Edition'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['core.Section'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('kicker', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table(u'core_feed')

        # Deleting model 'PublishingSchedule'
        db.delete_table(u'core_publishingschedule')

        # Deleting model 'Section'
        db.delete_table(u'core_section')

        # Deleting model 'Edition'
        db.delete_table(u'core_edition')

        # Deleting model 'Article'
        db.delete_table(u'core_article')


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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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